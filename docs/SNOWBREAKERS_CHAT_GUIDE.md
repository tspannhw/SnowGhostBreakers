# 💬 SnowBreakers AI Chat - User Guide

## 🎯 Overview

The **SnowBreakers AI Chat** is an intelligent conversational interface powered by Snowflake Cortex AI that allows you to interact with ghost detection data using natural language.

## ✨ Features

### **🤖 Conversational AI**
- Natural language understanding
- Context-aware responses
- Real-time data analysis
- Powered by Snowflake Cortex (`mistral-large2`)

### **📊 Data-Driven Insights**
- Automatic database context loading
- Ghost statistics and trends
- Recent activity monitoring
- Pattern recognition

### **💡 Quick Questions**
Pre-built question templates in sidebar:
- Ghost counts and statistics
- Common ghost types
- Threat level assessments
- Paranormal hotspots
- Activity patterns
- Investigation metrics

### **🔧 Advanced Features**
- **Direct SQL Query Execution**: Run custom queries directly from the chat
- **Chat Export**: Save conversations as JSON
- **Clear Chat**: Reset conversation history
- **Context Awareness**: AI remembers conversation flow

---

## 🚀 Getting Started

### **1. Access the Chat**
Navigate to **💬 SnowBreakers Chat** in the sidebar

### **2. Start Asking Questions**
Type any question about ghost data in the chat input, such as:
- "How many ghosts have we detected?"
- "What's the most dangerous ghost type?"
- "Show me activity trends this week"

### **3. Use Quick Questions**
Click any suggested question in the sidebar for instant answers

---

## 📝 Example Conversations

### **Example 1: Basic Statistics**

**You:** "How many ghosts have we detected?"

**SnowBreakers AI:** 
```
👻 Based on our current database:

📊 Ghost Statistics:
- Total Ghosts Registered: 45
- Unique Ghost Types: 8
- Average Threat Level: 3.2

The most common type is Poltergeist (15 instances), followed by 
Apparition (12 instances). Would you like to know more about any 
specific ghost type?
```

### **Example 2: Threat Analysis**

**You:** "Which ghosts are most dangerous?"

**SnowBreakers AI:**
```
⚠️ High-Threat Ghosts Analysis:

Top 5 Most Dangerous:
1. 👻 Shadow Demon (Threat Level: 5) - 3 instances
2. 👻 Vengeful Spirit (Threat Level: 5) - 2 instances
3. 👻 Poltergeist Alpha (Threat Level: 4) - 1 instance

🔍 Threat Distribution:
- Extreme (Level 5): 8 ghosts
- High (Level 4): 12 ghosts
- Medium (Level 3): 15 ghosts

💡 Recommendation: Extreme-threat entities require specialized 
containment protocols and experienced investigators.
```

### **Example 3: Pattern Recognition**

**You:** "What patterns do you see in recent activity?"

**SnowBreakers AI:**
```
📈 Recent Activity Patterns (Last 7 Days):

🕐 Temporal Patterns:
- Peak activity: 2 AM - 4 AM (40% of sightings)
- Lowest activity: 12 PM - 2 PM (5% of sightings)

📍 Location Patterns:
- Hotspot #1: Abandoned Hospital - 12 sightings
- Hotspot #2: Old Cemetery - 8 sightings
- Hotspot #3: Victorian Mansion - 6 sightings

👻 Ghost Type Trends:
- Poltergeist activity increased 30% vs. previous week
- Apparition sightings stable
- Shadow figures reported in new locations

🔍 Notable: Increased activity correlates with lunar cycle 
(full moon approaching).
```

---

## 💡 Best Practices

### **Asking Effective Questions**

#### **✅ Good Questions (Specific):**
- "How many high-threat sightings in the last 30 days?"
- "What's the average EMF reading for poltergeists?"
- "Show me investigation success rates by ghost type"
- "Which locations have recurring paranormal activity?"

#### **❌ Less Effective (Too Vague):**
- "Tell me about ghosts"
- "What's happening?"
- "Show me data"

### **Follow-Up Questions**
The AI maintains conversation context:

```
You: "How many ghosts are in the database?"
AI: "We have 45 registered ghosts across 8 types."

You: "Which type is most common?"
AI: "Poltergeists are the most common with 15 instances..."

You: "What's their average threat level?"
AI: "Poltergeists have an average threat level of 3.4..."
```

---

## 🔧 Advanced Features

### **1. Direct SQL Queries**

Access the "🔧 Advanced Features" expander to run custom SQL:

```sql
-- Example: Find high-threat ghosts
SELECT ghost_name, ghost_type, threat_level
FROM GHOST_DETECTION.APP.GHOSTS
WHERE threat_level >= 4
ORDER BY threat_level DESC;
```

The AI will execute the query and display results in a table format.

### **2. Export Conversations**

Click **💾 Export Chat** to save your conversation:

**Exported JSON Format:**
```json
{
  "timestamp": "2025-10-17T14:30:00",
  "messages": [
    {
      "role": "user",
      "content": "How many ghosts have we detected?"
    },
    {
      "role": "assistant",
      "content": "We have 45 registered ghosts..."
    }
  ]
}
```

### **3. Clear Chat History**

Click **🗑️ Clear Chat** to reset the conversation and start fresh.

---

## 📊 Data Context

The AI automatically loads and uses:

### **1. Ghost Statistics**
- Total ghost count
- Unique ghost types
- Average threat levels

### **2. Recent Activity**
- Sightings in last 7 days
- Latest sighting timestamp
- Activity trends

### **3. Top Categories**
- Most common ghost types
- High-frequency locations
- Threat distributions

---

## 🎯 Use Cases

### **1. Investigation Planning**
```
You: "What areas should we prioritize for investigation?"
AI: Identifies high-activity locations and recent hotspots
```

### **2. Resource Allocation**
```
You: "How many extreme-threat ghosts require containment?"
AI: Provides counts and recommendations
```

### **3. Trend Analysis**
```
You: "Has ghost activity increased this month?"
AI: Compares current vs. historical data
```

### **4. Evidence Review**
```
You: "What types of evidence do we have for poltergeists?"
AI: Lists evidence types and quality metrics
```

### **5. Team Performance**
```
You: "Which investigator has the highest success rate?"
AI: Analyzes investigation outcomes by team member
```

---

## 💬 Sample Queries

### **Statistics Queries**
- "How many ghosts of each type?"
- "What's the average threat level?"
- "Show me total sightings this year"
- "Count active investigations"

### **Analysis Queries**
- "Find correlations between EMF and ghost types"
- "What time of day has most activity?"
- "Which locations have multiple ghost types?"
- "Analyze investigation success factors"

### **Comparison Queries**
- "Compare this month to last month"
- "Which ghost type is most dangerous?"
- "Best vs. worst investigation outcomes"
- "Hottest vs. coldest paranormal locations"

### **Recommendation Queries**
- "Where should we investigate next?"
- "What equipment do we need for [ghost type]?"
- "How to handle a [threat level] ghost?"
- "Best strategy for [location type]?"

---

## 🔍 Context Awareness

The AI understands:

### **Database Schema**
- Table structures
- Column names
- Relationships
- Data types

### **Domain Knowledge**
- Ghost types and characteristics
- Threat level meanings
- Investigation procedures
- Evidence types

### **Current State**
- Recent activity
- Active investigations
- Resource availability
- Trend directions

---

## ⚠️ Limitations

### **What the AI CAN Do:**
✅ Answer questions about data in the database
✅ Provide statistical analysis
✅ Identify patterns and trends
✅ Suggest SQL queries
✅ Explain ghost characteristics
✅ Recommend investigation strategies

### **What the AI CANNOT Do:**
❌ Access data not in the database
❌ Make definitive paranormal judgments
❌ Guarantee investigation outcomes
❌ Predict future ghost activity with certainty
❌ Modify database records

---

## 🎨 Interface Elements

### **Chat Window**
- User messages (your questions)
- AI responses (blue chat bubbles)
- Thinking indicator (🤔 spinner)
- Error messages (if any)

### **Sidebar**
- Quick question buttons
- Instant access to common queries
- One-click question injection

### **Controls**
- **Chat Input**: Type your questions
- **Clear Chat**: Reset conversation
- **Export Chat**: Save as JSON
- **Advanced Features**: SQL execution

### **Expanders**
- **🔧 Advanced Features**: Direct SQL access
- **💡 Usage Tips**: Help and examples

---

## 🚀 Performance Tips

### **For Faster Responses:**
1. Ask specific questions (not overly broad)
2. Use quick questions for common queries
3. Break complex analyses into multiple questions
4. Cache frequently used queries in your workflow

### **For Better Answers:**
1. Provide context if needed
2. Specify time ranges for temporal queries
3. Name specific ghost types or locations
4. Ask follow-up questions for clarification

---

## 🔐 Security & Privacy

### **Data Access**
- AI only accesses authorized database views
- No modification of ghost records
- Query execution logged for audit
- Session-based conversation storage

### **Chat History**
- Stored in session state (not persisted)
- Cleared on page refresh
- Export feature for manual saving
- No automatic cloud backup

---

## 📞 Support

### **Common Issues**

**Issue:** "AI response is generic"
**Solution:** Provide more specific questions with context

**Issue:** "Query execution failed"
**Solution:** Check SQL syntax in Advanced Features

**Issue:** "Chat is slow"
**Solution:** Reduce database context scope or simplify queries

**Issue:** "Export not working"
**Solution:** Ensure browser allows downloads

---

## 🎉 Success Stories

### **Investigation Team Lead:**
> "I use SnowBreakers Chat every morning to get a quick briefing on overnight activity. Saves me 30 minutes of manual querying!"

### **Data Analyst:**
> "The ability to ask follow-up questions makes trend analysis so much faster. It's like having a paranormal data scientist on call."

### **Field Investigator:**
> "Before going to a location, I ask the chat about historical sightings there. Helps me prepare the right equipment."

---

## 🎯 Quick Reference

| Action | How To |
|--------|--------|
| Ask Question | Type in chat input and press Enter |
| Use Suggestion | Click quick question button in sidebar |
| Run SQL | Open Advanced Features → Enter query → Execute |
| Export Chat | Click 💾 Export Chat button |
| Clear History | Click 🗑️ Clear Chat button |
| Get Help | Open 💡 Usage Tips expander |

---

## 🔮 Future Enhancements

Coming soon:
- Voice input/output
- Chart generation from queries
- Automated report creation
- Investigation recommendations
- Multi-language support
- Mobile optimization
- Integration with external APIs

---

✅ **You're ready to start using SnowBreakers Chat!**

**Pro Tip:** Start with the quick questions to get familiar with the AI's capabilities, then progress to more complex custom queries.

👻 Happy ghost hunting! 🔍

