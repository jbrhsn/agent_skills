---
title: "How We Cut Latency by 80%"
theme: clean_minimal
cover:
  ratio: "wide"
---

# How We Cut Latency by 80%

By switching to edge caching and regional fallbacks, our platform reduced median p99 latency from 800ms to 160ms.

## The Problem: Centralized Database Bottleneck

Our original architecture funneled all requests through a single central database in us-east-1, creating unavoidable latency for international users.

> "We were losing customers in Asia-Pacific due to 2+ second response times. This wasn't a feature problem—it was a geography problem." — Sarah Chen, VP Infrastructure

## Solution: Edge-First Caching

We implemented a three-tier caching strategy:

1. **Local cache**: 1ms in-memory lookup
2. **Regional cache**: Redis clusters in 6 regions
3. **Global CDN**: CloudFlare edge network

## Results by the Numbers

- **94%** cache hit rate (up from 12%)
- **160ms** median p99 latency (down from 800ms)
- **2x** query reduction on primary DB
- **28%** reduction in infrastructure cost

## Technical Implementation

```python
def cached_fetch(key, ttl=3600):
    # Check local cache first (fastest)
    local = local_cache.get(key)
    if local:
        return local
    
    # Then regional cache
    regional = redis_pool.get(f"region:{region_id}:{key}")
    if regional:
        local_cache.set(key, regional, ttl)
        return regional
    
    # Finally, database
    result = db.query(key)
    redis_pool.set(f"region:{region_id}:{key}", result, ttl)
    return result
```

## Comparison: Before vs After

| Metric | Before | After |
|--------|--------|-------|
| p99 Latency | 800ms | 160ms |
| Cache Hit Rate | 12% | 94% |
| DB Query Load | 100% | 28% |
| Global Availability | 3 regions | 6 regions |
| Infrastructure Cost | $50k/month | $36k/month |

## What's Next

We're now exploring:
- Predictive prefetching of frequently accessed datasets
- Custom cache invalidation strategies per data type
- Automatic fallback routing during regional outages

The edge-first mentality isn't just about performance—it's fundamentally changing how we architect for a global user base.
