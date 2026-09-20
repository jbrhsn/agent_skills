# Kokoro v1.0 Voices — Quick Reference

54 voices across 8 languages as of Kokoro v1.0 (January 2025). Use the **Voice ID** as the `--voice` argument to `01_tts.py`.

Prefix key: `af` = American Female, `am` = American Male, `bf` = British Female, `bm` = British Male, `jf` = Japanese Female, `jm` = Japanese Male, `zf` = Mandarin Female, `zm` = Mandarin Male, `ef` = Spanish (ES) Female, `ff` = French Female.

---

## American English — Female (`af_`)

| Voice ID | Character | Best for |
|---|---|---|
| `af_heart` | Warm, conversational, clear | General narration — **recommended default** |
| `af_bella` | Energetic, upbeat | Social media, short-form content |
| `af_nicole` | Calm, measured, slightly formal | Educational, explainers |
| `af_sarah` | Friendly, approachable | Tutorials, how-to content |
| `af_sky` | Airy, soft, intimate | Lifestyle, wellness content |
| `af_nova` | Confident, authoritative | Business, thought leadership |
| `af_luna` | Gentle, slow-paced | Long-form narration |
| `af_stella` | Bright, expressive | Entertainment, storytelling |
| `af_aurora` | Deep, resonant | Documentary style |
| `af_ember` | Energetic, punchy | News, announcements |

## American English — Male (`am_`)

| Voice ID | Character | Best for |
|---|---|---|
| `am_adam` | Deep, clear, authoritative | Business, documentary |
| `am_echo` | Warm, laid-back | Podcast style, conversational |
| `am_eric` | Formal, measured | Corporate, educational |
| `am_fenrir` | Rich, confident | Thought leadership |
| `am_liam` | Young, casual | Consumer tech, startup content |
| `am_michael` | Professional, neutral | News, informational |
| `am_onyx` | Deep, dramatic | High-impact hooks |
| `am_puck` | Playful, lighthearted | Entertainment, humour |
| `am_santa` | Warm, grandfatherly | Seasonal, family content |

## British English — Female (`bf_`)

| Voice ID | Character | Best for |
|---|---|---|
| `bf_alice` | Crisp, polished, formal | Finance, tech, editorial |
| `bf_emma` | Friendly, approachable British | International audiences |
| `bf_isabella` | Elegant, measured | Luxury, culture, arts |
| `bf_lily` | Bright, lively | Lifestyle, travel |

## British English — Male (`bm_`)

| Voice ID | Character | Best for |
|---|---|---|
| `bm_daniel` | Authoritative, clear | Documentary, journalism |
| `bm_fable` | Rich, storytelling | Long-form narrative |
| `bm_george` | Warm, reassuring | Corporate, education |
| `bm_lewis` | Youthful, energetic | Consumer content |

## Japanese (`jf_` / `jm_`)

| Voice ID | Gender | Notes |
|---|---|---|
| `jf_alpha` | F | Standard Japanese narration |
| `jf_gongitsune` | F | Soft, expressive |
| `jf_nezumi` | F | Bright, youthful |
| `jf_tebukuro` | F | Warm, mature |
| `jm_kumo` | M | Clear, formal |

## Mandarin Chinese (`zf_` / `zm_`)

| Voice ID | Gender | Notes |
|---|---|---|
| `zf_xiaobei` | F | Clear, standard Mandarin |
| `zf_xiaoni` | F | Warm, conversational |
| `zm_yunjian` | M | Formal, authoritative |
| `zm_yunxi` | M | Youthful, energetic |
| `zm_yunxia` | M | Deep, measured |
| `zm_yunyang` | M | Neutral, broadcast style |

## Spanish — European (`ef_`)

| Voice ID | Gender | Notes |
|---|---|---|
| `ef_dora` | F | Clear, standard Castilian |

## French (`ff_`)

| Voice ID | Gender | Notes |
|---|---|---|
| `ff_siwis` | F | Standard French narration |

---

## Choosing a voice

1. **Match the content tone** — warm voices (`af_heart`, `am_echo`) for conversational content; authoritative voices (`af_nova`, `am_adam`, `bf_alice`) for business or documentary.
2. **Match the audience region** — prefer native-accent voices for region-specific content when possible.
3. **Test before committing** — generate a 5-second sample of the hook sentence with two or three candidate voices before synthesizing the full transcript.
4. **Do not promise voice quality rankings** — these characterizations are editorial descriptions, not measured evaluations. Actual quality depends on the specific text and is best judged by listening.

---

## Resources

- Official Kokoro repository: `hexgrad/Kokoro-82M` on Hugging Face
- ONNX model and voices: `onnx-community/Kokoro-82M-v1.0-ONNX` on Hugging Face
- `kokoro-onnx` Python package: `thewh1teagle/kokoro-onnx` on GitHub

