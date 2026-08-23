#!/usr/bin/env bash
# kwfetch.sh — keyless keyword harvesting + heuristic scoring.
# No API key, no login. See ../references/endpoints.md for endpoint details.
#
# Usage:
#   kwfetch.sh all "<seed>" [-e entity]... [-o out.tsv] [--deep] [--ddg]
#                           [--gl US] [--hl en] [--se-site stackoverflow]
#   kwfetch.sh score <raw.tsv>
#   kwfetch.sh suggest "<query>"      # single Google+Bing lookup
#   kwfetch.sh related "<term>"       # Datamuse only
#   kwfetch.sh entity "<term>"        # Wikipedia opensearch + pageviews
#   kwfetch.sh questions "<term>"     # Stack Exchange
#
# Output (all): TSV  source <TAB> term <TAB> rank_or_score
# Exit 0 even on partial failure; unavailable sources are logged to stderr.

set -uo pipefail

UA="${KW_UA:-kwfetch/1.0 (keyword-research skill; contact: set KW_UA env var)}"
HL="en"; GL="US"; SE_SITE="stackoverflow"
DEEP=0; DDG=0; SLEEP="${KW_SLEEP:-0.4}"
OUT=""; ENTITIES=()

log()  { printf '%s\n' "$*" >&2; }
have() { command -v "$1" >/dev/null 2>&1; }

for dep in curl jq; do
  have "$dep" || { log "FATAL: '$dep' is required but not installed."; exit 2; }
done

GET() { curl -sS -m 15 -A "$UA" "$@" 2>/dev/null; }

# ---------------------------------------------------------------- Tier 2

g_suggest() { # $1=query -> suggestions, one per line
  GET -G --data-urlencode "q=$1" \
      "https://suggestqueries.google.com/complete/search?client=firefox&hl=${HL}&gl=${GL}&ie=utf-8&oe=utf-8" \
    | jq -r '.[1][]?' 2>/dev/null
}

b_suggest() {
  GET -G --data-urlencode "query=$1" "https://api.bing.com/osjson.aspx" \
    | jq -r '.[1][]?' 2>/dev/null
}

ddg_related() {
  GET -G --data-urlencode "q=$1" "https://html.duckduckgo.com/html/" \
    | grep -oE 'class="related-searches__item"[^>]*>[^<]+' \
    | sed 's/.*>//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
    | grep -v '^$'
}

# ---------------------------------------------------------------- Tier 1

datamuse() { # $1=param ($2=value) -> "word<TAB>score"
  GET -G --data-urlencode "$1=$2" --data-urlencode "max=50" \
      "https://api.datamuse.com/words" \
    | jq -r '.[]? | "\(.word)\t\(.score // 0)"' 2>/dev/null
}

wiki_titles() {
  GET -G --data-urlencode "search=$1" \
      "https://en.wikipedia.org/w/api.php?action=opensearch&limit=10&format=json&namespace=0" \
    | jq -r '.[1][]?' 2>/dev/null
}

pv_window() { # sets PV_START / PV_END = last 12 full months
  if date -u -d "1 month ago" +%Y%m01 >/dev/null 2>&1; then
    PV_START=$(date -u -d "13 months ago" +%Y%m01)
    PV_END=$(date -u -d "1 month ago" +%Y%m01)
  else
    PV_START=$(date -u -v-13m +%Y%m01)
    PV_END=$(date -u -v-1m +%Y%m01)
  fi
}

wiki_views() { # $1=article title -> "mean<TAB>first<TAB>last"
  local enc; enc=$(printf '%s' "${1// /_}" | jq -sRr @uri)
  GET "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/${enc}/monthly/${PV_START}/${PV_END}" \
    | jq -r '[.items[]?.views] | select(length>0)
             | "\((add/length)|floor)\t\(.[0])\t\(.[-1])"' 2>/dev/null
}

stackx() { # $1=query -> "title<TAB>votes"
  curl -sS -m 20 --compressed -A "$UA" -G \
    --data-urlencode "q=$1" --data-urlencode "order=desc" \
    --data-urlencode "sort=votes" --data-urlencode "site=${SE_SITE}" \
    --data-urlencode "pagesize=25" \
    "https://api.stackexchange.com/2.3/search/advanced" 2>/dev/null \
    | jq -r '.items[]? | "\(.title)\t\(.score)"' 2>/dev/null
}

# ---------------------------------------------------------------- harvest

MODIFIERS_SUFFIX=(for vs with without "how" "why" "what" "is" "can" best tools
                  tutorial example alternatives guide explained "not working" 2026)
MODIFIERS_PREFIX=("how to" "why" "what is" "best" "when to" "should i")
ALPHA=(a b c d e f g h i j k l m n o p q r s t u v w x y z)

emit() { # $1=source $2=stream-with-optional-rank
  awk -v s="$1" 'BEGIN{FS=OFS="\t"} NF{ if(NF<2) $2=NR; print s,$1,$2 }'
}

harvest_autocomplete() { # $1=seed
  local q ok_g=0 ok_b=0
  local queries=("$1")
  for m in "${MODIFIERS_SUFFIX[@]}"; do queries+=("$1 $m"); done
  for m in "${MODIFIERS_PREFIX[@]}"; do queries+=("$m $1"); done
  if [ "$DEEP" -eq 1 ]; then
    for c in "${ALPHA[@]}"; do queries+=("$1 $c"); done
  fi

  local buf
  for q in "${queries[@]}"; do
    buf=$(g_suggest "$q" | awk 'NF{print $0"\t"NR}')
    if [ -n "$buf" ]; then printf '%s\n' "$buf" | emit google; ok_g=$((ok_g+1)); fi
    sleep "$SLEEP"
  done
  for q in "$1" "$1 vs" "how to $1" "best $1"; do
    buf=$(b_suggest "$q" | awk 'NF{print $0"\t"NR}')
    if [ -n "$buf" ]; then printf '%s\n' "$buf" | emit bing; ok_b=$((ok_b+1)); fi
    sleep "$SLEEP"
  done
  [ "$ok_g" -gt 0 ] && log "  ok   google-suggest ($ok_g/${#queries[@]} queries returned data)" \
                    || log "  FAIL google-suggest (0 of ${#queries[@]} queries returned data)"
  [ "$ok_b" -gt 0 ] && log "  ok   bing-autosuggest ($ok_b/4)" \
                    || log "  FAIL bing-autosuggest"
}

cmd_all() {
  local seed="$1"; shift
  log "seed: $seed"
  pv_window

  log "[1/5] autocomplete (tier 2)"
  harvest_autocomplete "$seed"
  for e in "${ENTITIES[@]:-}"; do
    [ -z "$e" ] && continue
    g_suggest "$e" | awk 'NF{print $0"\t"NR}' | emit google
    sleep "$SLEEP"
  done

  if [ "$DDG" -eq 1 ]; then
    log "[1b] duckduckgo related (tier 2, optional)"
    local d; d=$(ddg_related "$seed")
    if [ -n "$d" ]; then printf '%s\n' "$d" | emit ddg; log "  ok   duckduckgo"
    else log "  FAIL duckduckgo (no related-searches block found)"; fi
  fi

  log "[2/5] datamuse (tier 1)"
  local dm; dm=$(datamuse ml "$seed"; datamuse rel_trg "$seed")
  for e in "${ENTITIES[@]:-}"; do
    [ -z "$e" ] && continue
    dm+=$'\n'"$(datamuse rel_trg "$e")"
  done
  if [ -n "${dm// /}" ]; then printf '%s\n' "$dm" | grep -v '^$' | emit datamuse
    log "  ok   datamuse"
  else log "  FAIL datamuse"; fi

  log "[3/5] wikipedia opensearch (tier 1)"
  local wt; wt=$(wiki_titles "$seed")
  for e in "${ENTITIES[@]:-}"; do
    [ -z "$e" ] && continue
    wt+=$'\n'"$(wiki_titles "$e")"
  done
  if [ -n "${wt// /}" ]; then
    printf '%s\n' "$wt" | grep -v '^$' | sort -u | awk 'NF{print $0"\t0"}' | emit wikipedia
    log "  ok   wikipedia-opensearch"
  else log "  FAIL wikipedia-opensearch"; fi

  log "[4/5] wikimedia pageviews (tier 1, real numbers)"
  local any_pv=0
  while IFS= read -r t; do
    [ -z "$t" ] && continue
    local v; v=$(wiki_views "$t")
    if [ -n "$v" ]; then
      printf 'pageviews\t%s\t%s\n' "$t" "$(printf '%s' "$v" | cut -f1)"
      any_pv=1
    fi
  done < <(printf '%s\n' "$wt" | grep -v '^$' | sort -u | head -8)
  [ "$any_pv" -eq 1 ] && log "  ok   wikimedia-pageviews" \
                      || log "  FAIL wikimedia-pageviews (no matching articles)"

  log "[5/5] stack exchange (tier 1, technical topics)"
  local sx; sx=$(stackx "$seed")
  if [ -n "${sx// /}" ]; then printf '%s\n' "$sx" | emit stackexchange
    log "  ok   stackexchange (site=$SE_SITE)"
  else log "  FAIL stackexchange (no results or non-technical topic)"; fi

  log "done. tier2=observed/unofficial, tier1=official API. See scoring.md for grades."
}

# ---------------------------------------------------------------- scoring

cmd_score() {
  local f="$1"
  [ -f "$f" ] || { log "FATAL: no such file: $f"; exit 2; }
  awk 'BEGIN{FS=OFS="\t"; print "term","score","breadth","best_rank","words","grade","sources"}
  {
    src=$1; term=tolower($2); metric=$3+0
    gsub(/^[ \t]+|[ \t]+$/,"",term)
    if (term=="" || length(term)<3) next
    if (!((term SUBSEP src) in seen)) {
      seen[term SUBSEP src]=1
      breadth[term]++
      srcs[term] = srcs[term] (srcs[term]==""?"":",") src
    }
    if (src=="google" || src=="bing" || src=="ddg") {
      if (metric>0 && (!(term in rank) || metric<rank[term])) rank[term]=metric
      tier2[term]=1
    }
    if (src=="datamuse" || src=="wikipedia" || src=="stackexchange") tier1[term]=1
    if (src=="pageviews") { pv[term]=1; tier1[term]=1 }
    if (breadth[term]>maxb) maxb=breadth[term]
  }
  END{
    if (maxb<1) maxb=1
    for (t in breadth) {
      n=split(t,w," ")
      spec = (n>=3 && n<=7) ? 1.0 : (n==2 ? 0.6 : 0.3)
      r = (t in rank) ? rank[t] : 0
      pos = (r>=1 && r<=10) ? (11-r)/10 : 0.3
      s = 45*(breadth[t]/maxb) + 30*pos + 25*spec

      if (pv[t] || (breadth[t]>=2 && tier1[t])) g="A"
      else if (tier1[t] && !tier2[t])            g="B"
      else if (tier2[t])                         g="C"
      else                                       g="D"

      printf "%s\t%d\t%d\t%s\t%d\t%s\t%s\n", t, (s+0.5), breadth[t], (r?r:"-"), n, g, srcs[t]
    }
  }' "$f" | { read -r hdr; printf '%s\n' "$hdr"; sort -t$'\t' -k2,2nr; }
}

# ---------------------------------------------------------------- cli

[ $# -lt 1 ] && { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
CMD="$1"; shift

ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    -e) ENTITIES+=("$2"); shift 2 ;;
    -o) OUT="$2"; shift 2 ;;
    --deep) DEEP=1; shift ;;
    --ddg) DDG=1; shift ;;
    --gl) GL="$2"; shift 2 ;;
    --hl) HL="$2"; shift 2 ;;
    --se-site) SE_SITE="$2"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) [ -z "$ARG" ] && ARG="$1"; shift ;;
  esac
done

[ -z "$ARG" ] && { log "FATAL: missing argument for '$CMD'"; exit 2; }

run() {
  case "$CMD" in
    all)       cmd_all "$ARG" ;;
    score)     cmd_score "$ARG" ;;
    suggest)   g_suggest "$ARG" | awk 'NF{print $0"\t"NR}' | emit google
               b_suggest "$ARG" | awk 'NF{print $0"\t"NR}' | emit bing ;;
    related)   pv_window; { datamuse ml "$ARG"; datamuse rel_trg "$ARG"; } | emit datamuse ;;
    entity)    pv_window
               wiki_titles "$ARG" | while IFS= read -r t; do
                 [ -z "$t" ] && continue
                 v=$(wiki_views "$t")
                 printf 'pageviews\t%s\t%s\n' "$t" "${v:-0}"
               done ;;
    questions) stackx "$ARG" | emit stackexchange ;;
    *) log "FATAL: unknown command '$CMD'"; exit 2 ;;
  esac
}

if [ -n "$OUT" ] && [ "$CMD" != "score" ]; then
  run > "$OUT"
  log "wrote $(wc -l < "$OUT" | tr -d ' ') rows -> $OUT"
else
  run
fi
