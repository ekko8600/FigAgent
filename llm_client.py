import requests
import json
from typing import List, Dict, Any, Optional


class DeepSeekClient:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        stream: bool = False
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def generate_visualization_code(
        self, 
        data_summary: str, 
        user_requirements: Optional[str] = None,
        previous_code: Optional[str] = None,
        feedback: Optional[str] = None,
        allow_multiple: bool = True,
        num_files: int = 1
    ) -> str:
        """生成可视化代码，支持单图或多图"""
        
        system_prompt = f"""You are an expert data visualization specialist. Your goal: Create beautiful, insightful visualizations that help users understand data structure, patterns, and key insights at a glance.

CORE PRINCIPLES:

1. BEAUTY & CLARITY
   - Use elegant, professional design that attracts attention
   - High contrast for readability
   - Balanced composition with proper spacing
   - Visually appealing color schemes

2. COMPARISON & ANALYSIS
   - Make comparisons obvious and easy
   - Highlight key differences and patterns
   - Use visual cues (colors, sizes, positions) to guide attention
   - Add reference lines (means, medians, benchmarks) when useful

3. DATA STRUCTURE INSIGHT
   - Show data distribution clearly
   - Reveal correlations and relationships
   - Display trends and patterns prominently
   - Make outliers and anomalies visible

4. ACTIONABLE INSIGHTS
   - Help users discover patterns quickly
   - Make conclusions obvious from the visual
   - Support data-driven decision making
   - Tell a clear story with the data

DESIGN GUIDELINES:

Visual Style:
- Figure size: 10-12 inches wide for single plots, 14-16 for multiple subplots
- DPI: 300 for sharp, publication-quality output
- Color palette: Use seaborn's 'Set2', 'husl', or custom gradients
- Backgrounds: Clean white or very light gray (#F8F9FA)
- Font: 'DejaVu Sans' or 'Arial', with clear hierarchy:
  * Main title: 16pt, bold
  * Subplot titles: 14pt, semibold
  * Axis labels: 12pt
  * Tick labels: 10pt
  * Annotations: 11pt

Layout & Spacing:
- Generous margins (use tight_layout or constrained_layout)
- Clear separation between subplots
- Legend outside plot area when possible
- Proper padding around text elements

Statistical Elements:
- Add mean/median lines with annotations
- Show confidence intervals or error bars
- Include sample sizes in titles/labels
- Display key statistics directly on plot

Comparison Features:
- Sort bars/categories by value for easy ranking
- Use grouped/stacked designs for multi-category comparison
- Add percentage change annotations
- Highlight max/min values with distinct colors
- Use consistent scales across related plots

Interactive Elements (via annotations):
- Label important data points
- Add value labels on bars/points
- Show percentage changes
- Include trend indicators (↑/↓)

Code Structure:
```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3)
plt.rcParams['font.family'] = 'DejaVu Sans'

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

# [Your plotting code here]
# Add comparisons, annotations, statistics

# Enhance appearance
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3, linestyle='--')

# Add clear title and labels
plt.title('Clear, Descriptive Title', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('X Label', fontsize=12, fontweight='semibold')
plt.ylabel('Y Label', fontsize=12, fontweight='semibold')

# Save with high quality
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='white')
```

IMPORTANT - AUTO-RECOMMENDATION MODE:
When user provides NO specific requirements, you MUST:
1. Analyze data characteristics intelligently
2. Choose the BEST chart type for the data (not just any chart)
3. Create comparisons even within single dataset (by categories, time, groups)
4. Add statistical insights (means, trends, distributions)
5. Make the visualization tell a story

Common Patterns:
- Numeric + Categories → Grouped/Stacked bar chart with sorted values
- Time series → Line chart with trend, moving average, key events marked
- Single numeric → Distribution plot + box plot + statistics
- Multiple numerics → Correlation heatmap + scatter matrix
- Categories only → Count plot with percentages, sorted by frequency

Output: Executable Python code in ```python``` blocks."""

        user_message = f"""Data Summary:
{data_summary}

"""
        
        if user_requirements:
            user_message += f"User Requirements:\n{user_requirements}\n\n"
            user_message += "IMPORTANT: Follow user requirements while maintaining beauty, clarity, and comparison features.\n\n"
        else:
            user_message += """NO specific requirements provided - Use your expertise to:
1. Select the MOST INSIGHTFUL chart type for this data
2. Create meaningful COMPARISONS (across categories, time, groups)
3. Add STATISTICAL INSIGHTS (means, medians, trends)
4. Make it BEAUTIFUL and EASY TO UNDERSTAND
5. Help users discover PATTERNS and draw CONCLUSIONS

Think: "What would make this data most valuable and understandable to the user?"
"""
        
        if previous_code and feedback:
            user_message += f"Previous Code:\n```python\n{previous_code}\n```\n\n"
            user_message += f"User Feedback:\n{feedback}\n\n"
            user_message += "Improve the code based on feedback while maintaining quality."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat_completion(messages, temperature=0.3)
        
        # 提取代码块
        code = self._extract_code_block(response)
        return code
    
    def generate_combined_visualization_code(
        self,
        combined_summary: str,
        user_requirements: Optional[str] = None,
        num_datasets: int = 1,
        data_dict: Optional[Dict] = None
    ) -> str:
        """生成多数据集综合可视化代码，智能判断是否需要多图"""
        
        system_prompt = """You are an elite data visualization expert specializing in multi-dataset comparative analysis. Your mission: Create stunning, insightful visualizations that make data comparisons crystal clear and patterns immediately obvious.

=== CORE OBJECTIVES ===

1. EFFORTLESS COMPARISON
   - Make differences between datasets jump out visually
   - Use strategic positioning, colors, and scales
   - Add direct comparison metrics (%, ratios, deltas)
   - Highlight winners/losers, trends, outliers

2. BEAUTIFUL & ENGAGING
   - Create visually stunning charts that users want to look at
   - Use sophisticated color schemes and layouts
   - Professional typography and spacing
   - Balanced, harmonious composition

3. PATTERN DISCOVERY
   - Make trends and patterns immediately visible
   - Show relationships between datasets
   - Reveal correlations and divergences
   - Display statistical insights prominently

4. DATA STORYTELLING
   - Guide viewer's attention to key insights
   - Create logical visual flow
   - Use annotations to highlight important findings
   - Make conclusions obvious without explanation

=== DESIGN EXCELLENCE ===

Visual Strategy:
- Figure size: 14-18 inches wide for multi-dataset comparisons
- DPI: 300 (publication quality)
- Color strategy:
  * Use DISTINCT colors for each dataset (Set2, tab10, or custom palette)
  * Consistent color mapping across all subplots
  * Use color intensity to show magnitude differences
- Background: Pure white (#FFFFFF) or subtle gray (#FAFBFC)
- Font hierarchy:
  * Main title: 18pt, bold - tells the main story
  * Subplot titles: 14pt, semibold - specific comparisons
  * Axis labels: 12pt, semibold
  * Annotations: 11pt
  * Dataset labels in legend: 11pt

Layout Philosophy:
- Grid layouts (2x2, 1x3, 2x3) for multiple views
- Generous spacing between subplots (hspace=0.3, wspace=0.3)
- Unified color scheme across all subplots
- Consistent scales when comparing same metrics
- Legend: Outside plot area, or shared for all subplots

Comparison Techniques:
- Side-by-side bars for direct comparison
- Overlaid lines with different styles/colors
- Small multiples for pattern comparison
- Difference/ratio plots to show relative changes
- Ranking/sorting to show best/worst performers
- Normalized scales when needed for fair comparison

Statistical Enrichment:
- Add mean/median lines for each dataset
- Show standard deviations or confidence bands
- Include sample sizes (n=X) in labels
- Display key statistics as text annotations
- Highlight statistical significance
- Show percentage differences between datasets

Annotations & Labels:
- Label max/min values for each dataset
- Add percentage change indicators
- Show trend directions (↑↓→)
- Annotate interesting data points
- Display summary statistics on plot
- Add data source info in subtitle

=== SINGLE vs MULTIPLE PLOTS STRATEGY ===

Generate ONE INTEGRATED PLOT when:
✓ Similar data structures enable direct comparison
✓ Shared metrics/units allow same scale
✓ Overlay creates clarity (e.g., time series)
✓ Side-by-side comparison is the main goal
✓ < 5 datasets with < 4 key variables each
→ Use: Multi-color bars, overlaid lines, or 2x2 subplot grid within single figure

Generate MULTIPLE PLOTS (2-4) only when:
⚠ Datasets have different scales/units requiring separate views
⚠ Showing both detail and overview is essential
⚠ Different relationship types need separate representations
⚠ Complexity would overwhelm single view
→ Save as: 'output_1.png', 'output_2.png', etc.

=== CODE TEMPLATE ===

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Style setup
sns.set_style("whitegrid")
sns.set_palette("Set2")  # or custom colors
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Data access
# data_dict = {{'file1.csv': df1, 'file2.csv': df2, ...}}
datasets = list(data_dict.items())

# Create figure (adjust size based on complexity)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Main Comparison Title', fontsize=18, fontweight='bold', y=0.98)

# Plot each comparison
for idx, (name, df) in enumerate(datasets):
    ax = axes[idx // 2, idx % 2]
    
    # [Your plotting code]
    # Add statistics, annotations
    
    # Style individual subplot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(f'Dataset: {{Path(name).stem}}', fontsize=14, fontweight='semibold')
    ax.grid(alpha=0.3, linestyle='--')

# Unified legend (if applicable)
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.98, 0.96))

plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='white')
```

=== AUTO-RECOMMENDATION MODE (CRITICAL) ===

When NO user requirements provided, you MUST:
1. Analyze ALL datasets' characteristics together
2. Identify the KEY comparison point (what should user compare?)
3. Choose chart type that makes comparison EFFORTLESS
4. Add statistical comparisons (means, correlations, rankings)
5. Highlight interesting patterns/differences
6. Make insights OBVIOUS - no deep analysis needed

Smart Choices:
- Similar numeric data → Grouped bar chart or overlaid lines (sorted by value)
- Time series → Multi-line chart with annotated key events/differences
- Distributions → Overlaid density plots + box plots + means
- Rankings → Horizontal bar chart sorted by value with labels
- Correlations → Scatter matrix or heatmap with annotations

Data Access Pattern:
```python
# Get all datasets
datasets = list(data_dict.items())
df1_name, df1 = datasets[0]
df2_name, df2 = datasets[1]

# Or iterate
for filename, df in data_dict.items():
    dataset_name = Path(filename).stem  # Clean name
    # Use df and dataset_name
```

Output: Beautiful, executable Python code in ```python``` blocks."""

        user_message = f"""Combined Data Summary:
{combined_summary}

Number of datasets: {num_datasets}

"""
        
        if user_requirements:
            user_message += f"User Requirements:\n{user_requirements}\n\n"
            user_message += """IMPORTANT: Follow requirements while ensuring:
- Beautiful, professional appearance
- Clear comparisons between datasets
- Statistical insights and patterns
- Easy-to-understand visual story
"""
        else:
            user_message += """NO specific requirements - This is your chance to shine! Create the BEST comparative visualization by:

1. UNDERSTAND: What's the most important comparison here?
2. CHOOSE: What chart type makes comparison effortless?
3. DESIGN: Make it beautiful and professional
4. ANNOTATE: Add statistics, highlights, insights
5. GUIDE: Make patterns and differences obvious

Remember:
- Users should understand key insights in 5 seconds
- Comparisons should be crystal clear
- Design should be stunning and professional
- Every element should serve a purpose

Think: "What would make a data analyst say 'WOW, this is exactly what I needed!'"
"""
        
        user_message += """
Final check before generating code:
✓ Is comparison strategy clear?
✓ Will patterns be immediately visible?
✓ Is it beautiful and professional?
✓ Are insights highlighted?
✓ Can user draw conclusions easily?

Now generate the visualization code!"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat_completion(messages, temperature=0.3, max_tokens=6000)
        code = self._extract_code_block(response)
        return code
    
    def suggest_visualizations(self, data_summary: str) -> List[str]:
        """建议适合的可视化类型"""
        system_prompt = "你是一个数据可视化顾问，根据数据特征建议最合适的可视化类型。"
        user_message = f"""数据摘要：
{data_summary}

请建议3-5种最适合这个数据集的可视化类型，并简要说明原因。
格式：可视化类型 - 原因"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat_completion(messages, temperature=0.5)
        suggestions = [line.strip() for line in response.split('\n') if line.strip() and '-' in line]
        return suggestions
    
    def _extract_code_block(self, text: str) -> str:
        """从文本中提取代码块"""
        if '```python' in text:
            start = text.find('```python') + 9
            end = text.find('```', start)
            return text[start:end].strip()
        elif '```' in text:
            start = text.find('```') + 3
            end = text.find('```', start)
            return text[start:end].strip()
        else:
            return text.strip()

