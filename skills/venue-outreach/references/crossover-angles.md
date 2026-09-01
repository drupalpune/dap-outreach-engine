# Crossover angles

One paragraph per `org_type`. This is the block that changes per target; the
rest of the mail is stable. Pick by `crossover_angle` if the row names one,
otherwise fall back to `org_type`. Never send the generic version if any of the
specific ones fit.

Rewrite the chosen paragraph in the org's own terms — swap in the stack they
actually use, the product they actually ship. A paragraph that could have been
sent to any of the sixty orgs on the list is a paragraph that reads as a mail
merge.

## Angle keys

`crossover_angle` in the CSV names one of these. Blank falls back to `org_type`.

| Key | Section | Typical `org_type` |
|---|---|---|
| `drupal-native` | Already in the community | agency, services |
| `wordpress-crossover` | Digital agency | agency |
| `php-oss` | Product engineering | product |
| `hiring-visibility` | Services / consulting | services |
| `footfall-programming` | Coworking | coworking |
| `students-exposure` | Education | edu |
| `reciprocal` | Another community | community |
| `generic` | Fallback | other |

---

## `drupal-native` — they already build Drupal

> You already live in this ecosystem, so there is not much for me to sell here.
> The room is your peers, your team gets a morning of it without leaving the
> building, and hosting is the easiest way for the wider community to see how
> {{org_name}} works. If anyone on your side wants a slot on the agenda, that is
> open too.

Use for Drupal agencies and shops. **Skip the pitch entirely.** Explaining what
Drupal is to a Drupal agency reads as a mail merge that did not check who it was
writing to. Make it short, peer to peer, and offer them a speaking slot in the
same breath.

---

## `product` — product engineering company

> Most of your engineers work in one stack all week. A morning like this puts
> them in a room with people solving the same problems in Drupal, Laravel and
> plain PHP — and the exposure runs both ways, since the community gets to see
> how a product team does it. No travel, no ticket, they just come downstairs.

Use when: the org builds and ships its own software. Lean on the exposure and
the cross-pollination, not on brand.

## `services` — services / consulting / IT firm

> You are hiring for CMS and PHP work, and this is a room full of exactly those
> people spending a Saturday morning on their own craft. Hosting puts your name
> in front of them without a job post — and your own team gets a technical
> morning without a training budget line.

Use when: their careers page has open CMS/PHP/Drupal roles. Hiring-adjacent, but
never say "recruiting event" — the moment it reads as a hiring funnel, attendance
drops. Say visibility.

## `agency` — digital agency, WordPress / Drupal shop

> You already build on open source, so this is your community as much as ours.
> There is a lot of overlap between the WordPress and Drupal worlds — same
> hosting problems, same editor-experience arguments, same client conversations —
> and the sessions tend to be more useful the more mixed the room is. Your team
> would fit right in.

Use when: the org's business is building sites for clients, especially on
WordPress. This is the framing that worked in the July mail. Name the specific
CMS they use.

## `coworking` — coworking / community space

> A free technical meetup on a Saturday morning is footfall from exactly the
> people you want holding memberships, and it costs you a room that is quiet
> that day anyway. We handle speakers, promotion and RSVPs; your space gets
> named in every post. We run it clean and clear out by 13:30.

Use when: community programming is their product. Usually the fastest yes.
Lead with the operational lightness.

## `edu` — college, university, training institute

> Your students get a room full of working engineers talking about production
> systems, not coursework — which is a kind of exposure that is hard to
> timetable. Final-year students and recent alumni are welcome to attend, and
> the sessions are pitched at people who ship rather than at a syllabus.

Use when: engineering colleges and training institutes. Foreground the students.
Weekend access is the thing to nail down early.

## `community` — another tech community, user group, foundation

> Our calendars barely overlap and our audiences do, so this is closer to a
> swap than an ask. Happy to return it — a slot at a DAP meetup for one of your
> speakers, or a cross-post to our list when you run your next event.

Use when: another meetup group, foundation chapter, or open-source community.
Make it reciprocal. Offer something back in the first mail.

## `other` — fallback

> We are looking for a room in Pune for a free, monthly technical meetup — about
> thirty developers, a Saturday morning, wrapped up by 13:30. We handle
> everything except the space. If that is something you would be open to, I can
> send over the details.

Use only when nothing above fits. If you find yourself here often, the ICP needs
a new segment — add it to this file rather than sending the generic version twice.
