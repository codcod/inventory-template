---
source: # where this lifecycle is documented, e.g. a wiki page URL
fetched: # YYYY-MM-DD
notes: >
  Example lifecycle shipped with the template. Replace it with your organization's own
  stages. If you change slugs, also update tools/generate_pdf.py (PHASE_* constants)
  and library/templates/raw_note_template.md.
---

# Product & Delivery Lifecycle

The delivery lifecycle is a value stream — a connected flow of thinking, building, and
learning that takes an idea from raw possibility to something real in the hands of
users. It is not a rigid conveyor belt: ideas can be stopped at any point. If
discovery shows the problem isn't worth solving, or ideation surfaces a solution that
can't be justified, stopping early is the right outcome. The goal is thin slices of
value delivered incrementally. The lifecycle has five sequential stages:
**Idea → Discovery → Ideation → Development & Delivery → GTM**.

______________________________________________________________________

## Stage: Idea

**Slug:** `idea`

> Capture and triage concepts worth exploring; qualify them against strategic goals
> before committing to discovery work.

### Activities

- Submit a concept — new feature, process improvement, user pain, or strategic
  opportunity — to the idea backlog
- Write a problem-focused description: what the idea is, why it matters, what problem
  it solves
- Attach indicative impact and effort scores
- Link to relevant goals or strategic priorities
- Check for duplicate ideas before submitting
- Review the backlog on a regular cadence: promote, park, or close ideas
- Agree a time-box for discovery once an idea is accepted

### Typical roles

- Anyone (submit ideas)
- Product Manager (ongoing review, scoring, refinement)
- Product leadership (structured review; accept / deprioritise)

### Typical artefacts

- Idea in the backlog (summary, description, impact/effort scores, goal alignment)
- Feature ticket (created when the idea is accepted)

______________________________________________________________________

## Stage: Discovery

**Slug:** `discovery`

> Understand the problem before committing to a solution; test risky assumptions and
> produce enough clarity to decide confidently whether and how to proceed.

### Activities

- Explore the problem space; identify and prioritise risky assumptions
- Conduct user research, interviews, competitive analysis, and data review
- Define the feature: problem statement, personas, risky assumptions, initial scope,
  dependencies
- Start the product requirements document (PRD)
- Size the work across technical complexity, unknowns, dependencies, and compliance
  impact
- Decompose the feature into epics
- Identify dependencies on other teams, platforms, or third parties
- Make a proceed / pause / stop decision

### Typical roles

- Product Manager (feature owner; PRD author)
- Design / User Research (research, problem framing)
- Engineering Lead (feasibility, dependency mapping, sizing)
- Architecture / Security / Compliance (where relevant)

### Typical artefacts

- PRD (started; living document throughout)
- Size estimate
- Initial epic breakdown

______________________________________________________________________

## Stage: Ideation

**Slug:** `ideation`

> Shape potential solutions from the validated problem; design and test concepts;
> produce a clear solution direction and a ready story backlog.

### Activities

- Design solution concepts and lo-fi prototypes; iterate rapidly
- Test concepts with users; assess value vs. effort and feasibility
- Refine the PRD with the agreed solution direction and success metrics
- Produce designs covering required devices and states
- Run refinement sessions: shape epics into stories, agree API contracts, surface
  risks
- Write testable acceptance criteria — functional and non-functional
- Verify stories meet the Definition of Ready before sprint planning

### Typical roles

- Product Manager (PRD owner; story authoring)
- Design (concepts, user testing, final designs)
- Engineering (refinement, technical criteria, feasibility)
- Quality (acceptance-criteria quality, testability)

### Typical artefacts

- Refined PRD with solution direction and success metrics
- Designs (all devices and states)
- User stories with testable acceptance criteria
- Definition of Ready

______________________________________________________________________

## Stage: Development & Delivery

**Slug:** `development-and-delivery`

> Build and validate the solution in iterative sprints, delivering incremental
> releasable value; every change carries its own evidence of correctness.

### Activities

- Plan ready stories into sprints
- Write, review, test, and deploy code
- Validate technical proofs of concept where needed
- Write and maintain automated tests (unit, integration, UI)
- Implement monitoring, analytics, and observability
- Apply accessibility standards
- Use feature flags for safe incremental deployment
- Run automated linting, formatting, and type checks on every change
- Verify the Definition of Done at story and epic level
- Retire deprecated code, flags, and systems

### Typical roles

- Engineering (code, tests, review, deployment)
- Quality (test strategy, automation)
- Product Manager (story review, acceptance)
- Design (accessibility and design-system compliance)

### Typical artefacts

- Production-ready code, deployed behind feature flags
- Test suites
- Monitoring dashboards, alerts, and runbooks
- Definition of Done
- Technical decision records

______________________________________________________________________

## Stage: GTM

**Slug:** `gtm`

> Release into production; coordinate go-to-market; confirm monitoring; measure
> outcomes; and retire features that no longer serve users.

### Activities

- Enable the feature for a controlled production release
- Coordinate go-to-market: marketing, user communications, support enablement
- Confirm monitoring is active before and after release
- Smoke test the live production state
- Measure adoption and outcomes against the PRD success criteria
- Update the PRD with actual outcomes and learnings
- Produce tutorials, walkthroughs, or release notes
- Deprecate features that no longer serve users

### Typical roles

- Product Manager (GTM coordination, measurement)
- Engineering (release, feature flags, monitoring)
- Marketing / Comms (external communications)
- Customer Support (enablement, tutorials)
- Analytics (outcome measurement)

### Typical artefacts

- Production release
- Go-to-market materials (release notes, communications, tutorials)
- PRD updated with measured outcomes
