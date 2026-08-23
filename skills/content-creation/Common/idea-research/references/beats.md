# Beats

The fixed topic set. Ideas outside these score zero on beat fit and are dropped.

Edit this file to change coverage — the fetchers and scorer read it at runtime, so no
code changes are needed.

| Beat | Keywords (matched against titles) | Subreddits | Medium tags |
|---|---|---|---|
| AI | ai, llm, gpt, claude, agent, rag, prompt, model, inference, fine-tune, openai, anthropic, embedding, transformer | artificial, LocalLLaMA, MachineLearning, singularity, ChatGPT | artificial-intelligence, machine-learning, llm |
| Data engineering | data engineering, pipeline, etl, elt, warehouse, dbt, airflow, spark, duckdb, snowflake, lakehouse, streaming, kafka, orchestration | dataengineering, datascience, database | data-engineering, data-science, big-data |
| Finance | market, valuation, fed, inflation, earnings, interest rate, recession, bond, equity, macro | finance, investing, economics | finance, investing, economy |
| Personal finance | budget, savings, retirement, index fund, debt, salary, fire movement, side income, tax, mortgage, frugal | personalfinance, financialindependence, Fire | personal-finance, money, financial-independence |
| Writing | writing, writer, newsletter, blog, essay, editing, storytelling, substack, medium, publishing | writing, Blogging, Substack | writing, blogging, creativity |
| Productivity | productivity, workflow, focus, habits, note-taking, obsidian, notion, time management, automation, deep work | productivity, ObsidianMD, notion, getdisciplined | productivity, self-improvement, work |
| Product reviews | review, hands-on, benchmark, comparison, vs, tried, tested, alternative, migrating from, switched to | SaaS, software, apps, selfhosted | product-review, software, tools |
| Thought leadership | future of, why i, lessons from, what nobody, the real reason, hard truth, career, hiring, layoff, remote work, leadership | cscareerquestions, ExperiencedDevs, startups | leadership, career-advice, entrepreneurship |

## Beat fit scoring

A candidate's beat fit = the beat with the most keyword hits in its title.

- 3+ distinct keyword hits → 20 pts
- 2 hits → 14 pts
- 1 hit → 8 pts
- 0 hits → 0 pts, dropped from results

Cross-beat ideas (e.g. "AI for data pipelines", "LLM tools for writers") score on
their best-matching beat but are worth flagging to the user — intersection topics
tend to be less saturated than either beat alone.

## Personal edge

The strongest ideas sit where a trending topic meets something the user has actually
done. When presenting ideas, prefer angles the user can write from experience over
ones requiring pure research — Medium's 2026 curation actively deprioritizes generic
AI-generated coverage, and first-hand specifics are what clears that bar.
