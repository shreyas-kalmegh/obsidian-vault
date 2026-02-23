I recently joined Crowdstrike as Data analytics engineer and was applying for Senior data engineer / Data engineer 2 (L4/L5) roles for last 6 months (interviewed at Uber, Amazon, Doordash got rejected at all places) been lurking in this sub for that time and wanted to share my experience , last company was salesforce (7 YOE)

Crowdstrike interview

HR reached out via Linkedin after applying

HR screening

General role and skillset understanding

Round 1 - Hiring manager round

Previous roles and responsibilities along with major projects executed most of the call was around projects, A data pipeline around pulling data from a location and he kept asking questions on tooling and added some scenarios like archiving, backfilling, data quality, schema change etc.

Round 2 - Technical round

3 people panel was there and call lasted for nearly 2 hours

Python - for loop based name lookup (easy)

SQL - Question started as Pandas question which I didnt knew so said will do it in sql and can use AI to translate it to pandas if required at end , were fine for SQL basic case/ coalese / group by question with null and error (division by zero) handling , some data related questions that what happens to code if this type of row comes were asked so had to work on data quality tests for it

Stakeholder management and scenario based questions

Round 3 - Skip Level Manager

Various STAR based scenario and discussion about roles and responsibilities for crowdstrike

Overall one of the easiest rounds I gave(NO DSA) and the process took about 5-6 weeks, but the friendliest bunch of folks so that really drawed me in to accept the offer along with being remote for now

Previous TC - ~55 , Crowdstrike TC - ~77

Other than crowdstrike gave interviews at Uber, Amazon, Disney, Doordash, Adyen, Netskope, Ebay , albertsons

Here is my application Sankey

Some pointers to share from my interview experience

Application and resume

Fortunately as I was already at a good product company calls were there but most didnt had budget so applying from Naukri didnt help I used career portal (most imp), linkedin , 6figr, uplers, instahyre to apply

Customised resume to job requirements helped as generic resume was mostly rejected need to have keywords aligning to job requirements and the tool coverage if possible

Referrals didnt help me as nowhere I applied through referral called me back but at least it helps in getting noticed as recruiter for sure looks at your profile even if its glancery

Technical

DSA is most important as I was rejected from Uber , Disney Amazon, Ebay due to it not just the solution but optimal solution , only easy mediums no hards

Topics I remeber were hashmap, tree, graph, recursion, stack, heap, two pointers, sorting, binary search

SQL will be hards didnt face recursion but sessionisation, gap islands, running sum, group by having and row number were there think about data too while wrinting query and ask questions if possible so as to not miss any flags in where clause

No AI tooling was allowed in interviews and even though I had some projects around it no questions were asked just DE fundamentals were expected

Data modelling

Practice with AI for the basic 5-6 businesses (eCommerce, cab , food delivery, social media , banking/finance) and for big tech prepare data model for their business and understand the north star metrics a business would have like eCommerce has retention and social media has engagment rather than focussing on making things strictly star or snowflake focus on metric you want to track/analyse and refine after discussion with interviewer

Pipeline/System design

I have only worked for batch so don't have steaming experience nor faced it in interviews so I just mention we can use pub sub to land this data in S3 that's it after that I have one standard pipeline I use everywhere based on there stack I am comfortable with as the interviewer is not looking at you to nail the tooling they are looking that do you understand tradeoffs so prepare that (for eg I prepared snowflake vs databricks but was not ready when someone asked why not redshift as rest of stack is aws so we would get discount for using it ) overall just be ready to explain your why before every decision

Hiring manager

⭐️⭐️⭐️ use Star and focus on your action and result a lot don't be afraid to inflate your results but don't go overboard and be clear what part of project you want to ownership of as mostly it's given that you are not owning end to end , try to have some questions

If possible don't go blank when you a chance to ask something I mostly go with generic what is the role about and try to align my current exp saying oh this thing I have worked in past in this way , this works on my experience but if you are junior just try to show your enthusiasm and don't be just silent listener when they speak and most importantly be clear and refine your communication for this round as soft skill has most weightage in this round

Resources used

I am a reading heavy person

Books - DDIA , Data warehouse toolkit , Data engineering design patterns, deciphering data architectures None of them cover to cover just bits and pieces

Blogs - Uber, slack , doordash, aws etc engineering blogs

Youtube - Manish Kumar,Afaque ahmad, Love Babbar

DSA - Leetcode (Neetcode 150, Blind 75), Neetcode, Algo monster

SQL - Datalemur, leetcode , stratascratch

