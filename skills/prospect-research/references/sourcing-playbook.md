# Sourcing playbook

Where to look, roughly in order of hit rate.

## Venue leads

### 1. Your own history (best)

`data/venues.csv` rows at `warm`, and `data/meetups.csv` past hosts. A previous
host saying yes again is the cheapest venue you will ever get. Check this before
any web search.

### 2. People you've met

Conference badges, community WhatsApp groups, past attendees' employers. A named
opening line — "we met at DrupalCamp in March" — outperforms everything else in
this file. If the lead came from a person, the `source` column should say so.

### 3. Orgs that host other communities

Whoever hosted the last PHP, WordPress, Python, JS, or DevOps meetup in Pune has
already solved weekend access and internal approval. Meetup.com past events for
Pune tech groups is the fastest way to find them.

### 4. Careers pages

Search for Pune companies hiring Drupal, PHP, or CMS developers. A live job post
is a live budget and a reason to want engineers in the building.

### 5. Engineering blogs

A Pune company with a technical blog has someone whose job includes developer
brand. The post authors are your contacts — and they're speaker leads too.

### 6. Drupal.org

Organisation profiles listing Pune, and user profiles with Pune in them. Small
pool, very high fit.

### 7. Coworking spaces

Baner, Hinjewadi, Kharadi, Viman Nagar, Koregaon Park. Community programming is
their product; a Saturday morning is dead time. Often the fastest yes, and the
right fallback when a cycle is running late.

### 8. Cold company lists

Last resort. Low hit rate, and it burns names you might want later through a
warmer door.

## Speaker leads

1. **Past speakers** — `speakers.csv` at `spoke`, 90 days on. Warmest bench you have.
2. **Attendees who ask good questions.** Note names on the day; this is where most first-time speakers come from.
3. **Conference speaker lists** — DrupalCon, DrupalCamp India, PHP and open-source conferences. Anyone who has spoken once will consider speaking again.
4. **Module and package maintainers** the community actually uses.
5. **Engineering-blog authors** — they've done the hard part already; a talk is a rewrite.
6. **Host-org engineers.** Ask every confirmed host whether someone on their team wants a slot. Very high hit rate, and it deepens the host relationship.

## Qualifying, fast

Three questions:

1. Is there a room for 25–30 people and weekend access?
2. Is there anyone inside who would enjoy saying yes?
3. Is it under an hour from the city centre?

Two nos and it's `not_a_fit`. Write the reason in `notes` — future you will want
to know whether it was distance or indifference.

## Discipline

Eight to ten researched leads per cycle. This is a small pool of Pune orgs you
will keep running into for the next decade; the system should make you more
personal per mail, not let you send more of them. Thirty first-touches a month
means something has gone wrong.
