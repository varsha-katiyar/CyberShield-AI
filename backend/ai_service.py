
"""
Google Gemini AI Service for CyberShield-AI
Provides intelligent threat analysis, risk assessment, and security recommendations
"""
import os
import json
from typing import Optional, Dict, Any
import google.generativeai as genai


class GeminiAIService:
    """Service for interacting with Google Gemini API for cybersecurity analysis"""

    def __init__(self):
        """Initialize the Gemini AI service with API key from environment"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable not set. "
                "Get your API key from https://makersuite.google.com/app/apikey"
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def analyze_threat(
        self,
        behavior_score: float,
        nlp_score: float,
        network_score: float,
        url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze threat levels using Gemini AI and provide detailed insights
        """
        try:
            prompt = self._build_threat_analysis_prompt(
                behavior_score, nlp_score, network_score, url
            )

            response = self.model.generate_content(prompt)
            analysis_text = response.text

            parsed_analysis = self._parse_threat_analysis(analysis_text)
            return {
                "success": True,
                "threat_analysis": parsed_analysis,
                "raw_response": analysis_text,
            }
        except Exception as e:
            print(f"Error in analyze_threat: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "threat_analysis": self._generate_fallback_analysis(
                    behavior_score, nlp_score, network_score
                ),
            }

    def generate_security_recommendations(
        self, threat_level: str, threat_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate AI-powered security recommendations based on threat analysis
        """
        try:
            # Simplify threat level for prompt
            threat_level_str = str(threat_level).lower().strip()
            
            prompt = f"""You are a cybersecurity expert. Generate 3-4 actionable security recommendations for a {threat_level_str} threat level.

RESPOND ONLY WITH VALID JSON, NO MARKDOWN OR OTHER TEXT:
{{
    "immediate_actions": ["action 1", "action 2", "action 3"],
    "preventive_measures": ["measure 1", "measure 2", "measure 3"],
    "monitoring_suggestions": ["suggestion 1", "suggestion 2"],
    "risk_explanation": "brief explanation"
}}"""

            response = self.model.generate_content(prompt)
            recommendations_text = response.text.strip()
            
            print(f"Debug: Raw recommendations response: {recommendations_text[:100]}...")

            parsed = self._parse_json_response(recommendations_text)
            
            # Check if we got valid recommendations
            if isinstance(parsed, dict) and "immediate_actions" in parsed:
                return {
                    "success": True,
                    "recommendations": parsed,
                }
            else:
                print(f"Debug: Could not extract recommendations, using fallback")
                return {
                    "success": False,
                    "recommendations": self._get_fallback_recommendations(threat_level_str),
                }
                
        except Exception as e:
            print(f"Error in generate_security_recommendations: {str(e)}")
            return {
                "success": False,
                "recommendations": self._get_fallback_recommendations(threat_level),
            }

    def _get_fallback_recommendations(self, threat_level: str) -> Dict[str, Any]:
        """Return fallback recommendations when AI fails"""
        threat_level = str(threat_level).lower().strip()
        
        recommendations_map = {
            "critical": {
                "immediate_actions": [
                    "Isolate affected system from network immediately",
                    "Preserve forensic evidence and initiate incident response",
                    "Notify security team and stakeholders",
                    "Activate business continuity procedures"
                ],
                "preventive_measures": [
                    "Implement additional network segmentation and monitoring",
                    "Strengthen multi-factor authentication",
                    "Conduct immediate security audit and patch management",
                    "Deploy advanced threat detection systems"
                ],
                "monitoring_suggestions": [
                    "Enable 24/7 monitoring on critical systems",
                    "Track all access and anomalous behavior patterns",
                    "Set up real-time alerting for similar threats",
                    "Review and strengthen incident response procedures"
                ],
                "risk_explanation": "Critical threat requires immediate action to prevent system compromise."
            },
            "high": {
                "immediate_actions": [
                    "Conduct detailed threat assessment and analysis",
                    "Implement temporary security controls",
                    "Document all findings and evidence",
                    "Prepare incident response and mitigation plan"
                ],
                "preventive_measures": [
                    "Apply security patches and updates",
                    "Strengthen access controls and authentication",
                    "Increase system monitoring and logging",
                    "Review and update security policies"
                ],
                "monitoring_suggestions": [
                    "Increase monitoring frequency on affected systems",
                    "Track recurring threat patterns and indicators",
                    "Review security logs and audit trails daily",
                    "Conduct regular incident response drills"
                ],
                "risk_explanation": "High-level threat requires prompt investigation and mitigation actions."
            },
            "medium": {
                "immediate_actions": [
                    "Investigate threat source and nature",
                    "Document findings and impact assessment",
                    "Consider and implement security updates",
                    "Review user access permissions"
                ],
                "preventive_measures": [
                    "Keep systems updated with latest patches",
                    "Implement security best practices",
                    "Conduct security awareness training",
                    "Review and strengthen access controls"
                ],
                "monitoring_suggestions": [
                    "Monitor system performance and activity",
                    "Review security logs on regular schedule",
                    "Track security metrics and trends",
                    "Test backup and recovery procedures"
                ],
                "risk_explanation": "Medium-level threat should be addressed with standard security measures."
            },
            "low": {
                "immediate_actions": [
                    "Continue monitoring the situation",
                    "Apply routine security updates",
                    "Document observations for records",
                    "Maintain standard security practices"
                ],
                "preventive_measures": [
                    "Maintain current security posture",
                    "Apply updates and patches as scheduled",
                    "Continue security training programs",
                    "Keep security policies updated"
                ],
                "monitoring_suggestions": [
                    "Continue standard system monitoring",
                    "Review logs as per normal schedule",
                    "Maintain security hygiene practices",
                    "Track overall system health"
                ],
                "risk_explanation": "Low-level threat - maintain standard security practices and monitoring."
            }
        }
        
        return recommendations_map.get(threat_level, recommendations_map["medium"])

    def explain_anomaly(self, anomaly_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable explanation of detected anomalies
        """
        try:
            prompt = f"""Explain this security anomaly in simple terms (2-3 sentences):

Anomaly Data: {json.dumps(anomaly_data, indent=2)}"""

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate explanation: {str(e)}"

    def assess_url_safety(self, url: str) -> Dict[str, Any]:
        """
        Assess the safety of a given URL using AI analysis
        """
        try:
            prompt = f"""Assess the security of this URL: {url}

Return JSON with:
{{
    "safety_score": 0-100,
    "risk_level": "safe|warning|dangerous",
    "concerns": ["concern1", "concern2"],
    "recommendations": ["recommendation1"]
}}

RESPOND ONLY WITH JSON:"""

            response = self.model.generate_content(prompt)
            return {
                "success": True,
                "assessment": self._parse_json_response(response.text),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _build_threat_analysis_prompt(
        self, behavior_score: float, nlp_score: float, network_score: float, url: Optional[str]
    ) -> str:
        """Build the prompt for threat analysis"""
        url_context = f"URL/Domain: {url}\n" if url else ""

        return f"""Analyze this threat data and return ONLY JSON:

{url_context}
Behavior Score: {behavior_score}/100
NLP Score: {nlp_score}/100
Network Score: {network_score}/100

Return valid JSON only:
{{
    "overall_risk_level": "low|medium|high|critical",
    "risk_score": {int((behavior_score + nlp_score + network_score) / 3)},
    "threat_summary": "brief summary",
    "threat_indicators": ["indicator1", "indicator2"],
    "affected_areas": ["area1"],
    "confidence": "high",
    "key_insights": ["insight1"]
}}"""

    def _parse_threat_analysis(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from threat analysis response"""
        return self._parse_json_response(response_text)

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from AI response text
        Handles cases where JSON might be wrapped in markdown code blocks
        """
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                try:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                except:
                    pass
            elif "```" in response_text:
                try:
                    json_str = response_text.split("```")[1].split("```")[0].strip()
                    return json.loads(json_str)
                except:
                    pass
            
            # Try to find JSON object in the text
            try:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = response_text[start:end]
                    return json.loads(json_str)
            except:
                pass
            
            # Return empty structure
            return {
                "error": "Could not parse AI response",
                "raw_response": response_text[:200],
            }

    def _generate_fallback_analysis(
        self, behavior_score: float, nlp_score: float, network_score: float
    ) -> Dict[str, Any]:
        """Generate analysis when AI call fails"""
        avg_score = (behavior_score + nlp_score + network_score) / 3

        if avg_score < 30:
            risk_level = "low"
        elif avg_score < 60:
            risk_level = "medium"
        elif avg_score < 80:
            risk_level = "high"
        else:
            risk_level = "critical"

        return {
            "overall_risk_level": risk_level,
            "risk_score": int(avg_score),
            "threat_summary": f"Anomaly detected with average risk score of {avg_score:.1f}",
            "threat_indicators": [
                f"Behavioral: {behavior_score}/100",
                f"Content: {nlp_score}/100",
                f"Network: {network_score}/100",
            ],
            "affected_areas": ["User account", "System activity"],
            "confidence": "medium",
            "key_insights": ["Unusual activity pattern detected"],
            "fallback": True,
        }


def get_ai_service() -> Optional[GeminiAIService]:
    """Factory function to get AI service instance"""
    try:
        return GeminiAIService()
    except ValueError as e:
        print(f"AI Service initialization failed: {str(e)}")
        return None