from src.Dissertation.taxonomy import (IndustryTaxonomy,
                                       RetentionTaxonomy,
                                       DigitalTechTaxonomy)


class LiteratureReviewPrompt:
    def __init__(self, abstract):
        self.prompt_template = {
            "Cmd_Ext_Activity_Deepseek": f"""
You are an expert academic researcher. Please read the following abstract and extract such elements in JSON format:  
\- "challenges": the main problem or gap addressed  
\- "methods": the research methods used  
\- "findings": Key results or outcomes  
\- "industries": {IndustryTaxonomy.industry_taxonomy_sci_prompt['prompt']}    
\- "correlation": the correlation between the research object in this paper and knowledge retention, the scope of value from 0 to 1
\- "knowledge flows": SECI model discussed, the scope of value: {RetentionTaxonomy.SECI_taxonomy}
\- "tacit knowledge types": Tacit knowledge discussed, the scope of value: {RetentionTaxonomy.collins_based_tacit_knowledge_taxonomy}  
\- "activities": the knowledge retention approaches discussed, the preferred scope of value:  {RetentionTaxonomy.knowledge_retention_activities_taxonomy}. If the abstract clearly indicates another academically valid knowledge-retention practice not listed above, use the more appropriate term instead.
\- "technologies": Digital technologies discussed, the scope of value: {DigitalTechTaxonomy.digital_technology_taxonomy} . If the abstract clearly indicates another academically valid digital technologies not listed above, use the more appropriate term instead. 

Abstract:  
{abstract} 

Respond ONLY with a valid JSON object. Do not include any markdown formatting, code block indicators (like ```), backticks, the word 'json', or any other explanatory text. The response must start with {{ and end with }}.""",

            'Cmd_Ext_Activity_Gemini': f"""
You are an expert academic researcher specializing in knowledge management and research analysis. Carefully read the abstract provided and extract the requested elements. Return the results strictly in valid JSON format that follows the specified schema and rules.

Abstract:  
{abstract}  

Extraction Requirements are as follows:
Identify and extract:
\- "challenges" — The main research problem, gap, or issue addressed in the study.
\- "methods" — The research methods, approaches, or methodologies used.
\- "findings" — Key results, conclusions, or outcomes.
\- "industries" — Identify the relevant SIC industry classification (Division + Major Group).Select the best match from the list below: {IndustryTaxonomy.industry_taxonomy_sci_prompt['prompt']} . If none match exactly, choose the closest academically appropriate.
\- "correlation": the correlation between the research object in this paper and knowledge retention, the scope of value from 0 to 1
\- "knowledge flows" — SECI knowledge conversion processes mentioned. Preferred values:{RetentionTaxonomy.SECI_taxonomy}
\- "tacit knowledge types" — Types of tacit knowledge discussed.Preferred values: {RetentionTaxonomy.collins_based_tacit_knowledge_taxonomy}.
\- "activities" — Knowledge-retention approaches discussed.Preferred values:{RetentionTaxonomy.knowledge_retention_activities_taxonomy}. If the abstract clearly indicates another academically valid knowledge-retention practice not listed above, use the more appropriate term instead.
\- "technologies": — Digital technologies discussed. Preferred values:{DigitalTechTaxonomy.digital_technology_taxonomy}. If the abstract clearly indicates another academically valid digital technologies not listed above, use the more appropriate term instead. 

Output Format Rules (Strict)
Output must be only one valid JSON object. Do not include any markdown formatting, code block indicators (like ```), backticks, the word 'json', or any other explanatory text. The response must start with {{ and end with }}. Use this exact structure:
{{
  "challenges": "",
  "methods": [],
  "findings": "",
  "industries": {{
    "division": "",
    "majorGroup": ""
  }},
  "correlation": "",
  "knowledge_flows": "",
  "tacit knowledge types": [],
  "activities": [],
  "technologies": []
}}

Additional Interpretation Rules：
1. Base extracted content on explicit statements and conceptually aligned implications in the abstract. When academic constructs are not named verbatim but are strongly implied by described mechanisms, map them to the closest preferred value using domain reasoning. 
2. Use concise academic wording.
3. Lists must contain unique values only (no duplicates).
4. If a field is not mentioned, return an empty string ("") or empty array ([]) as appropriate.
5. Ensure terminology is standardized and formatted consistently across outputs so results remain comparable across repeated uses."""
}

    def get_prompt(self, cmd):
        return self.prompt_template[cmd]

if __name__ == '__main__':
    abstract = """
Traditional patient education often lacks personalization and engagement, potentially limiting knowledge acquisition and treatment adherence[1]. Advances in artificial intelligence (AI), including voice cloning technology and large language models such as ChatGPT, offer new opportunities to deliver personalized, scalable, and interactive health education[2-3]. However, evidence regarding the comparative effectiveness of different AI-based voice cloning strategies and the reliability of automated AI evaluation tools remains limited[4-5]. BACKGROUND Traditional patient education often lacks personalization and engagement, potentially limiting knowledge acquisition and treatment adherence[1]. Advances in artificial intelligence (AI), including voice cloning technology and large language models such as ChatGPT, offer new opportunities to deliver personalized, scalable, and interactive health education[2-3]. However, evidence regarding the comparative effectiveness of different AI-based voice cloning strategies and the reliability of automated AI evaluation tools remains limited[4-5].To evaluate the effectiveness of AI-assisted patient education integrating voice cloning and ChatGPT, to compare physician voice cloning with patient self-voice cloning, and to assess the reliability of ChatGPT as an automated evaluation tool for education outcomes. OBJECTIVE To evaluate the effectiveness of AI-assisted patient education integrating voice cloning and ChatGPT, to compare physician voice cloning with patient self-voice cloning, and to assess the reliability of ChatGPT as an automated evaluation tool for education outcomes.A prospective, three-arm, parallel-group randomized controlled trial.A total of 180 hospitalized patients requiring standardized health education were recruited from a tertiary hospital. Inclusion criteria were: age ≥18 years, clear diagnosis requiring health education, clear consciousness, and voluntary participation with informed consent. Exclusion criteria were: severe hearing impairment, severe cognitive impairment, expected hospitalization <3 days, or prior participation in similar studies.Participants were randomly assigned (1:1:1) to receive (1) traditional education (control), (2) AI-assisted education using physician voice cloning, or (3) AI-assisted education using patient self-voice cloning. All groups received identical educational content with equal duration.The primary outcome was education content compliance, evaluated using ChatGPT-4 with validated prompts and verified by expert review. Secondary outcomes included knowledge retention, education satisfaction, treatment adherence, quality of life (SF-36), and psychological status (Hospital Anxiety and Depression Scale).Participants were randomly allocated using a computer-generated random sequence. Due to the nature of the intervention, participants were not blinded; outcome assessors and data analysts were blinded to group allocation. METHODS A prospective, three-arm, parallel-group randomized controlled trial.A total of 180 hospitalized patients requiring standardized health education were recruited from a tertiary hospital. Inclusion criteria were: age ≥18 years, clear diagnosis requiring health education, clear consciousness, and voluntary participation with informed consent. Exclusion criteria were: severe hearing impairment, severe cognitive impairment, expected hospitalization <3 days, or prior participation in similar studies.Participants were randomly assigned (1:1:1) to receive (1) traditional education (control), (2) AI-assisted education using physician voice cloning, or (3) AI-assisted education using patient self-voice cloning. All groups received identical educational content with equal duration.The primary outcome was education content compliance, evaluated using ChatGPT-4 with validated prompts and verified by expert review. Secondary outcomes included knowledge retention, education satisfaction, treatment adherence, quality of life (SF-36), and psychological status (Hospital Anxiety and Depression Scale).Participants were randomly allocated using a computer-generated random sequence. Due to the nature of the intervention, participants were not blinded; outcome assessors and data analysts were blinded to group allocation.Of 180 randomized participants, 174 (96.7%) completed the trial. Both AI-assisted groups demonstrated significantly higher education content compliance immediately after education compared with the control group (physician voice: 86.7 ± 7.3; self-voice: 92.5 ± 6.8 vs control: 73.2 ± 8.5; P < 0.001). The patient self-voice group showed superior knowledge retention before discharge, higher education satisfaction, and greater treatment adherence compared with both the physician voice and control groups (all P ≤ 0.02). At one-month follow-up, the self-voice group maintained improved adherence (Cohen's d = 0.74) and exhibited significantly lower anxiety and depression scores (all P ≤0.02), along with improved SF-36 quality-of-life domains. ChatGPT-based evaluations demonstrated high reliability compared with expert assessments (weighted κ = 0.87, 95% CI 0.82-0.91). RESULTS Of 180 randomized participants, 174 (96.7%) completed the trial. Both AI-assisted groups demonstrated significantly higher education content compliance immediately after education compared with the control group (physician voice: 86.7 ± 7.3; self-voice: 92.5 ± 6.8 vs control: 73.2 ± 8.5; P < 0.001). The patient self-voice group showed superior knowledge retention before discharge, higher education satisfaction, and greater treatment adherence compared with both the physician voice and control groups (all P ≤ 0.02). At one-month follow-up, the self-voice group maintained improved adherence (Cohen's d = 0.74) and exhibited significantly lower anxiety and depression scores (all P ≤0.02), along with improved SF-36 quality-of-life domains. ChatGPT-based evaluations demonstrated high reliability compared with expert assessments (weighted κ = 0.87, 95% CI 0.82-0.91).This study introduces an innovative patient education model integrating AI voice cloning and ChatGPT, representing a novel approach distinct from previous studies that primarily relied on standard text-to-speech or professionally recorded content. The key innovation lies in utilizing patients' own cloned voices for health education delivery, leveraging the self-reference effect to enhance learning outcomes. Compared with prior research focusing on clinician-narrated content, this study provides the first empirical evidence that self-voice education produces superior outcomes across multiple domains including compliance, satisfaction, and psychological well-being. These findings contribute to the field by establishing a theoretical and practical framework for personalized AI-driven patient education. In real-world clinical settings, this approach offers a scalable, cost-effective solution to enhance patient engagement, particularly valuable in resource-limited environments where individualized education is challenging to deliver. CONCLUSIONS This study introduces an innovative patient education model integrating AI voice cloning and ChatGPT, representing a novel approach distinct from previous studies that primarily relied on standard text-to-speech or professionally recorded content. The key innovation lies in utilizing patients' own cloned voices for health education delivery, leveraging the self-reference effect to enhance learning outcomes. Compared with prior research focusing on clinician-narrated content, this study provides the first empirical evidence that self-voice education produces superior outcomes across multiple domains including compliance, satisfaction, and psychological well-being. These findings contribute to the field by establishing a theoretical and practical framework for personalized AI-driven patient education. In real-world clinical settings, this approach offers a scalable, cost-effective solution to enhance patient engagement, particularly valuable in resource-limited environments where individualized education is challenging to deliver.Trial Registration: Chinese Clinical Trial Registry (ChiCTR2500101882); registration application initiated on January 15, 2025 and finalized on April 30, 2025, before participant enrollment began in May 2025. CLINICALTRIAL Trial Registration: Chinese Clinical Trial Registry (ChiCTR2500101882); registration application initiated on January 15, 2025 and finalized on April 30, 2025, before participant enrollment began in May 2025.
    """
    obj = LiteratureReviewPrompt(abstract)
    print(obj.get_prompt('Cmd_Ext_Activity_Gemini'))