AI Engineer Assessment — Customer Support Chatbot
The Situation
You're an AI engineer at Meridian Electronics, a mid-size company that sells computer products — monitors, keyboards, printers, networking gear, and accessories. The support team currently handles all customer inquiries by phone and email, and leadership wants to explore whether an AI-powered chatbot could handle common requests: checking product availability, helping customers place orders, looking up order history, and authenticating returning customers.
The backend team has already built an internal services layer and exposed it as an MCP server so that an LLM-based chatbot can call into existing business systems without direct database access:
MCP_SERVER_URL=https://order-mcp-74afyau24q-uc.a.run.app/mcp
Transport: Streamable HTTP
Your engineering manager has asked you to build a working prototype and present it to the team by the end of day. The VP of Customer Experience will also be watching — she wants to understand whether this is worth investing in before next quarter's planning.
Your Assignment
Build a deployable, production-ready prototype of the customer support chatbot. "Production-ready" means: if the demo goes well, engineering should be able to take your code, do a security review, and push it to production without a rewrite. Think clean architecture, appropriate error handling, tested behavior, and thoughtful decisions — not just "does it work."
Constraints
LLM: Use a cost-effective model (flash or mini tier — e.g., Gemini Flash, GPT-4o-mini, Claude Haiku). The business case only works if per-conversation costs stay low.
UI: At minimum, a functional chat interface (Gradio, Streamlit, or equivalent). If you have time, a full UI framework (Next.js, etc.) would strengthen the demo.
Deployment: At minimum, deploy to HuggingFace Spaces so the team can try it live. Bonus for deployment to Vercel, GCP, AWS, or Azure.
Scope: Connect to the MCP server, discover its available tools, and build a chatbot that uses them to serve Meridian's customers. The MCP tools define what the chatbot can do — explore them and make sure your bot handles those workflows well.
Time
You have 3 hours. You won't be able to do everything perfectly — that's by design. How you prioritize is part of what we're evaluating. Budget your time accordingly.

Deliverables
Video 1 — Kickoff (submit by: {START TIME + 30 MINS})
You've just read the brief. Before writing any code, record a short video:
What's the business problem you're solving for Meridian?
What's your plan of attack? What will you build first, and what might you cut if you run out of time?
Video 2 — Mid-point check-in (submit by: {START TIME + 1 HR 45 MINS})
You're partway through. Record a video covering:
What you've built so far and the decisions you've made
What you've done to correct or improve AI-generated code
Any challenges you've hit and how you're working through them
Video 3 — Final Presentation (submit by: {START TIME + 3 HRS})
You're presenting to your engineering manager and the VP of Customer Experience to pitch whether this prototype should move forward. This is the most important deliverable.
Length: 3–10 minutes
Your presentation should include:
A live demo of the chatbot handling real customer scenarios
A walkthrough of the code and technical architecture — focus on important decisions and show that you understand what the code is doing (not just that it runs)
Honest assessment: what works well, what are the limitations, and what would you improve with more time?
Final submission
Turn in:
Video 3
GitHub repo
Deployed chatbot URL
Screenshots of the solution in action
Timing
Submissions are due at the posted deadline
Full credit for on-time submission
Credit is reduced for every 20 minutes late
