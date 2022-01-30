### 5 de agosto de 2021, 11:11

Dear KGS's Admin,

TL;DR: Developing comparable skill estimates among various Go associations around the world through a minimum extract of the KGS database.

We are developing a skill estimator for the Argentine Go Association [1] (based on TrueSkill Through Time [2]) which, unlike the estimators commonly used in the video game industry (TrueSkill, Glicko, American Go Association), guarantees good initial estimates and comparability between estimates separated in time and space. The advantage of TrueSkill Through Time lies in its temporal causal model, which links all historical activities in the same Bayesian network, allowing the information to propagate correctly throughout the system.

Although this estimator guarantees comparability within each database, it does not guarantee comparability between estimates of Go associations that do not have their databases linked to each other. To make estimates comparable across databases it is necessary to link events by identifying common users. Many of the members of our association, as of many other Go associations around the world, are active users of KGS. This is an opportunity for KGS to be the reference point for various Go associations around the world. Go associations that link their database to the KGS database will obtain estimates that will be comparable to each other.

For this purpose, we are writing to ask you if it is possible to access an extract of the KGS database containing basic data of all games (without moves): game id, white id, black id, date, rules, handicap, komi, size, result, time limit, type.

Yours sincerely,

Gustavo Landfried.
Phd Computer Science.

[1] https://www.go.org.ar/
[2] https://github.com/glandfried/TrueSkillThroughTime

### 6 de agosto de 2021, 17:42

Dear Gustavo
Thank you for your inquiry, I am not sure if this is feasible or not.  I will check with programmers,
Best wishes,
Shimari

### 3 de septiembre de 2021, 10:25

Dear Shimari

I bring into the conversation a professor of computer science, Dr.
Esteban Mocskos, a member of one of the largest computer science
institutes in Latin America.  As I told you, we need a minimum extract
of the KGS database to develop comparable skill estimates among
various Go associations around the world. Our implementation of
TrueSkill Through Time [1] correctly propagate the information
throughout the system allowing reliable initial estimates and
comparability between distant estimates. We would not want to overload
your server with too many queries. We understand that companies in the
United States have a policy of sharing information for research
purposes. If necessary, we could make the request through our
collaborators who live in the United States.

Yours sincerely,

Gustavo Landfried.
Phd student on Computer Science.

[1] https://github.com/glandfried/TrueSkillThroughTime