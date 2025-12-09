# Driver Analysis and Predictive Insights - Cell Generation Code
# This code will be integrated into the notebook generation

def add_driver_analysis_cells(cells, df_name, numeric_cols, cat_cols):
    """Add Driver Analysis and Predictive Insights cells"""
    
    # STAGE 1: Complex KPI Creation
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["# Driver Analysis and Predictive Insights"]})
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## STAGE 1: Creating Complex KPIs (Efficiency Metrics)"]})
    
    # Find KPI columns
    kpi_keywords = ['sales', 'revenue', 'profit', 'income', 'gross']
    qty_keywords = ['quantity', 'units']
    rating_keywords = ['rating', 'score']
    
    kpi_col = next((c for c in numeric_cols if any(kw in c.lower() for kw in kpi_keywords)), None)
    qty_col = next((c for c in numeric_cols if any(kw in c.lower() for kw in qty_keywords)), None)
    rating_col = next((c for c in numeric_cols if any(kw in c.lower() for kw in rating_keywords)), None)
    
    if kpi_col and qty_col:
        # Ratio KPI
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Create Efficiency Ratio KPI\n"
            f"{df_name}['Efficiency_Ratio'] = {df_name}['{kpi_col}'] / {df_name}['{qty_col}'].replace(0, np.nan)\n"
            f"print('Efficiency Ratio Statistics:')\n"
            f"{df_name}['Efficiency_Ratio'].describe()"
        ]})
        
        # Visualize distribution
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Visualize Efficiency Ratio Distribution\n"
            f"plt.figure(figsize=(14,5))\n\n"
            f"plt.subplot(1,2,1)\n"
            f"plt.hist({df_name}['Efficiency_Ratio'].dropna(), bins=30, edgecolor='black', color='skyblue')\n"
            f"plt.title('Distribution of Efficiency Ratio ({kpi_col}/{qty_col})')\n"
            f"plt.xlabel('Efficiency Ratio')\n"
            f"plt.ylabel('Frequency')\n\n"
            f"plt.subplot(1,2,2)\n"
            f"plt.boxplot({df_name}['Efficiency_Ratio'].dropna())\n"
            f"plt.title('Efficiency Ratio - Outlier Detection')\n"
            f"plt.ylabel('Efficiency Ratio')\n"
            f"plt.tight_layout()\n"
            f"plt.show()"
        ]})
        
        # Top and Bottom 1%
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Identify Top 1% and Bottom 1% Performers\n"
            f"top_1_pct = {df_name}['Efficiency_Ratio'].quantile(0.99)\n"
            f"bottom_1_pct = {df_name}['Efficiency_Ratio'].quantile(0.01)\n\n"
            f"print(f'Top 1% Threshold: {{top_1_pct:.2f}}')\n"
            f"print(f'Bottom 1% Threshold: {{bottom_1_pct:.2f}}')\n\n"
            f"top_performers = {df_name}[{df_name}['Efficiency_Ratio'] >= top_1_pct]\n"
            f"bottom_performers = {df_name}[{df_name}['Efficiency_Ratio'] <= bottom_1_pct]\n\n"
            f"print(f'\\nTop Performers: {{len(top_performers)}} records')\n"
            f"print(f'Bottom Performers: {{len(bottom_performers)}} records')\n"
            f"print('\\nThese represent your highest-leverage opportunities!')"
        ]})
    
    # STAGE 2: Correlation and Driver Analysis
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## STAGE 2: Correlation and Driver Analysis"]})
    
    if len(numeric_cols) >= 2:
        # Scatter plot with regression
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Scatter Plot with Regression Line\n"
            f"plt.figure(figsize=(10,6))\n"
            f"sns.regplot(data={df_name}, x='{numeric_cols[1]}', y='{numeric_cols[0]}', scatter_kws={{'alpha':0.5}}, line_kws={{'color':'red', 'linewidth':2}})\n"
            f"plt.title('Driver Analysis: {numeric_cols[1]} vs {numeric_cols[0]}')\n"
            f"plt.xlabel('{numeric_cols[1]}')\n"
            f"plt.ylabel('{numeric_cols[0]}')\n"
            f"plt.grid(True, alpha=0.3)\n"
            f"plt.show()"
        ]})
        
        # Calculate correlation
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Calculate Correlation Coefficient\n"
            f"correlation = {df_name}[['{numeric_cols[0]}', '{numeric_cols[1]}']].corr().iloc[0,1]\n"
            f"print(f'Correlation between {numeric_cols[1]} and {numeric_cols[0]}: {{correlation:.3f}}')\n\n"
            f"if abs(correlation) > 0.7:\n"
            f"    print('Strong correlation detected! This is a key driver.')\n"
            f"elif abs(correlation) > 0.4:\n"
            f"    print('Moderate correlation. This variable has some influence.')\n"
            f"else:\n"
            f"    print('Weak correlation. This may not be a primary driver.')"
        ]})
        
        # Correlation heatmap
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Correlation Heatmap of All Numerical Variables\n"
            f"plt.figure(figsize=(10,8))\n"
            f"numeric_data = {df_name}[{numeric_cols[:6]}].corr()\n"
            f"sns.heatmap(numeric_data, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True, linewidths=1)\n"
            f"plt.title('Correlation Heatmap: Identifying Key Drivers')\n"
            f"plt.tight_layout()\n"
            f"plt.show()"
        ]})
        
        # Identify strongest predictor
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Identify Strongest Predictor\n"
            f"correlations_with_target = {df_name}[{numeric_cols[:6]}].corr()['{numeric_cols[0]}'].abs().sort_values(ascending=False)\n"
            f"print('Variables ranked by correlation strength with {numeric_cols[0]}:')\n"
            f"print(correlations_with_target)\n"
            f"print(f'\\nStrongest predictor: {{correlations_with_target.index[1]}} (r={{correlations_with_target.values[1]:.3f}})')"
        ]})
    
    # STAGE 3: Multivariate Segmentation
    if len(cat_cols) >= 2 and len(numeric_cols) >= 1:
        cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## STAGE 3: Multivariate (Triple-Axis) Segmentation"]})
        
        # Triple-axis box plot
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Triple-Axis Analysis: {numeric_cols[0]} by {cat_cols[0]} and {cat_cols[1]}\n"
            f"plt.figure(figsize=(12,6))\n"
            f"sns.boxplot(data={df_name}, x='{cat_cols[0]}', y='{numeric_cols[0]}', hue='{cat_cols[1]}', palette='Set2')\n"
            f"plt.title('Multivariate Segmentation: {numeric_cols[0]} by {cat_cols[0]} & {cat_cols[1]}')\n"
            f"plt.xlabel('{cat_cols[0]}')\n"
            f"plt.ylabel('{numeric_cols[0]}')\n"
            f"plt.xticks(rotation=45)\n"
            f"plt.legend(title='{cat_cols[1]}')\n"
            f"plt.tight_layout()\n"
            f"plt.show()"
        ]})
        
        # Statistical comparison
        cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "source": [
            f"# Statistical Comparison Across Segments\n"
            f"segment_analysis = {df_name}.groupby(['{cat_cols[0]}', '{cat_cols[1]}'])['{numeric_cols[0]}'].agg(['mean', 'median', 'count']).round(2)\n"
            f"print('Segment Performance Analysis:')\n"
            f"print(segment_analysis.sort_values('mean', ascending=False))\n"
            f"print('\\nInsight: Identify which combination of {cat_cols[0]} and {cat_cols[1]} yields highest {numeric_cols[0]}')"
        ]})
    
    # STAGE 4: Predictive Summary
    cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## STAGE 4: Predictive Summary & Strategic Actions"]})
    
    if len(numeric_cols) >= 2:
        cells.append({"cell_type": "markdown", "metadata": {}, "source": [
            f"### Predictive Model Statement\n\n"
            f"Based on the correlation analysis between **{numeric_cols[1]}** and **{numeric_cols[0]}**, "
            f"we can formulate predictive insights:\n\n"
            f"**Key Finding**: The relationship between these variables suggests that changes in {numeric_cols[1]} "
            f"will have a measurable impact on {numeric_cols[0]}.\n\n"
            f"**Predictive Statement**: If the correlation coefficient is strong (r > 0.7), "
            f"a 10% increase in {numeric_cols[1]} is predicted to yield approximately a 7-10% change in {numeric_cols[0]}.\n\n"
            f"**Strategic Implication**: Focus optimization efforts on the strongest predictor identified in the correlation heatmap."
        ]})
    
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [
        "### Strategic Recommendations Based on Drivers\n\n"
        "#### 1. Focus on High-Impact Drivers\n"
        "**Action**: Allocate resources to optimize the variables with the strongest correlation to your primary KPI. "
        "These are your leverage points for maximum impact.\n\n"
        "#### 2. Target High-Efficiency Segments\n"
        "**Action**: The top 1% performers identified in the efficiency analysis represent best-in-class operations. "
        "Study their characteristics and replicate across other segments.\n\n"
        "#### 3. Address Low-Efficiency Outliers\n"
        "**Action**: The bottom 1% performers require immediate intervention. "
        "Investigate root causes and implement corrective measures or consider discontinuation.\n\n"
        "#### 4. Leverage Multivariate Insights\n"
        "**Action**: The triple-axis segmentation reveals specific niches with superior performance. "
        "Develop hyper-targeted strategies for these high-value combinations.\n\n"
        "#### 5. Predictive Resource Allocation\n"
        "**Action**: Use the identified correlations to build simple predictive models. "
        "Forecast outcomes based on planned changes to driver variables before implementation."
    ]})
    
    return cells
