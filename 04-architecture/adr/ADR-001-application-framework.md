# ADR-001: Use Flask as Application Framework

**Status:** Accepted  
**Date:** 2026-06-17  
**Deciders:** Project Team

---

## Context

We need a web framework for the Health Monitor application. The team has strong infrastructure/operations experience but limited software development experience. The application is intentionally simple — a dashboard with health endpoint and database integration.

## Decision

Use **Flask** with Jinja2 templates for server-rendered HTML.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Flask** | Simple, mature, team has Python scripting familiarity, excellent docs, Jinja2 built-in | Synchronous by default; less "modern" |
| FastAPI | Auto-docs, async support, type hints | Async complexity; better for APIs than server-rendered pages |
| Django | Batteries-included, admin panel | Over-engineered for a 5-route application; steep learning curve |
| React + API | Modern SPA; rich UI | Team cannot learn React in time; adds entire frontend build toolchain |

## Consequences

**Positive:**
- Team can be productive quickly (Python scripting background)
- Server-rendered templates eliminate frontend build complexity
- Mature ecosystem of Flask extensions (SQLAlchemy, Migrate, Prometheus)
- Production-proven (Netflix, LinkedIn, Pinterest use Flask)
- Gunicorn + Nginx is a standard production deployment pattern

**Negative:**
- No auto-generated API documentation (acceptable — few endpoints)
- Synchronous by default (acceptable — low traffic, health checks use APScheduler)
- Less modern than FastAPI (acceptable — reliability over trendiness)

**Risks:**
- None significant. Flask is well within team's capability.

---

*AI Assisted Engineering Framework v1.0*
