a list of key dimensions for models which connect to SWOT analysis:
VRIO (Resource-Based View)
    Checks whether a firm’s resources/capabilities give sustainable advantage.
    V – Valuable? (Does it help exploit opportunities or neutralize threats?)
    R – Rare? (Is it unique compared to competitors?)
    I – Inimitable? (Is it costly to copy or substitute?)
    O – Organized? (Is the firm structured to capture the value?)
    👉 Use this mainly for Strengths & Weaknesses.

Dynamic Capabilities (Teece, 2007)
    Focuses on how firms adapt to technological change.
    Sensing – Identifying new opportunities & threats.
    Seizing – Mobilizing resources to capture opportunities.
    Reconfiguring – Transforming or renewing capabilities to stay competitive.
    👉 Weak sensing = weakness; strong reconfiguring = strength.

Porter’s Five Forces
    Structures the external environment around competition.
    Threat of New Entrants
    Bargaining Power of Suppliers
    Bargaining Power of Buyers
    Threat of Substitutes
    Industry Rivalry (Competitors)
    👉 Use these to derive Opportunities & Threats.

Technology–Organization–Environment (TOE) Framework
    Explains adoption and performance of innovations.
    Technology: innovation’s features (complexity, compatibility, relative advantage).
    Organization: firm’s size, culture, resources, leadership support.
    Environment: industry, competition, regulation, customer demand.
    👉 Tech & Org = Strengths/Weaknesses; Env = Opportunities/Threats.

Innovation Radar (Sawhney et al., 2006)
    Looks at 12 dimensions of innovation (not just product).
    Offerings (what new products/services)
    Platform (common components leveraged)
    Solutions (integrated offerings for customers)
    Customers (new segments reached)
    Customer Experience (improved usability, service)
    Value Capture (new revenue models)
    Processes (new ways of operating)
    Organization (new structures, incentives, skills)
    Supply Chain (partnerships, sourcing)
    Presence (new channels, geographies)
    Networking (alliances, ecosystems)
    Brand (positioning, trust, identity)
    👉 Strengths = strong across multiple dimensions; Weaknesses = narrow focus.

TOWS Matrix
    Turns SWOT into strategy.
    SO strategies: Use strengths to seize opportunities.
    WO strategies: Overcome weaknesses with opportunities.
    ST strategies: Use strengths to reduce threats.
    WT strategies: Minimize both weaknesses & threats.

For a firm-level SWOT after tech innovation, combining two levels:
    Internal Lens: Use VRIO (RBV) + Dynamic Capabilities to assess Strengths/Weaknesses.
    External Lens: Use Five Forces or TOE to structure Opportunities/Threats.
    Strategic Synthesis: Apply TOWS to turn the analysis into strategies.

So the form of the survey is as following:
    Internal VRIO V – Valuable? (Does it help exploit opportunities or neutralize threats?)
    Internal VRIO R – Rare? (Is it unique compared to competitors?)
    Internal VRIO I – Inimitable? (Is it costly to copy or substitute?)
    Internal VRIO O – Organized? (Is the firm structured to capture the value?)
    Internal DC Sensing – Identifying new opportunities & threats.
    Internal DC Seizing – Mobilizing resources to capture opportunities.
    Internal DC Reconfiguring – Transforming or renewing capabilities to stay competitive.
    Internal EXQ   praised touch points
    Internal EXQ   negative pain points
    External EXQ   unmet expectations visible in discussions.
    External EXQ   complaints trending on social platforms.
    External PFF   Threat of New Entrants
    External PFF   Bargaining Power of Suppliers
    External PFF   Bargaining Power of Buyers
    External PFF   Threat of Substitutes
    External PFF   Industry Rivalry (Competitors)
    External TOE   Customer Requirement
    External TOE   regulation

face to different cases, we should replace the questionare questions with more real, specific questions.

challenges:
1. LLMs just search limited news from website, so the source of information may represent 
2. LLMs may beautify the performance 
3. LLMs may overlook the release time of news which plays a vital role in analysis

How to mitigate these issues.

For 1, 
- tell LLMs the websites which they should pay more attention to
- construct RAG

For 2,
- reasoning verification: split the reasons which LLMs provide, and add verification process.
    