# Market Pulse: Concept Note

## 1. Background and Rationale
Agriculture remains Uganda’s backbone, employing over 80 % of the population and contributing approximately 40 % of GDP. Yet smallholder farmers, particularly women and rural households suffer from volatile crop prices. Market prices for maize, beans, and coffee can fluctuate by 20–30 % within weeks due to rainfall, transport disruptions, or trader speculation.

Existing tools like Esoko, Kudu, and government SMS platforms disseminate current prices but either lack forecasting ability or local-language interfaces. Meanwhile, global AI models such as Agrocast and IBM Watson Agriculture use satellite and weather data but aren’t localized to Ugandan crops or languages.

Market Pulse leverages machine-learning forecasting and sentiment analysis to give farmers actionable predictions (“Sell next week”) with voice alerts in Luganda, bridging the gap between data science and everyday decision-making.

## 2. Problem Statement
Smallholder farmers in Uganda lack reliable, real-time price forecasts that incorporate weather, social, and market signals. Current tools stop at descriptive analytics and assume literacy and connectivity. As a result, farmers sell at sub-optimal times, losing up to 20 % of potential revenue.

## 3. Literature Review Summary

| Study/System | Method | Key Gap |
| :--- | :--- | :--- |
| Esoko (Ghana, 2015) | SMS dissemination of prices | No predictive modelling or sentiment integration. |
| Agrocast (Global, 2019) | Weather-based yield forecasting. | Focus on yield, not price; not localized. |
| Makerere AI Lab (2021) | Crop-disease detection via CNNs | Technical success, limited farmer interface. |
| Indian AI Price Predictors (2022–2023) | LSTM, ARIMA for price trends | No local-language or offline design; limited African data. |
| Twitter-Sentiment Crop Models (2023) | Combined LSTM + sentiment | High accuracy (~90 %), but datasets from developed economies. |

Hence, no Ugandan system combines time-series forecasting, sentiment analysis, weather data, and local-language voice advisory for smallholders.

## 4. Objectives
**Overall goal:**
To develop an AI-driven crop-price predictor that empowers Ugandan farmers to make data informed marketing decisions.

**Specific objectives:**
1. Build predictive models integrating historical price, weather, and social-media sentiment data.
2. Provide forecasts and simple advisories via text and Luganda voice.
3. Evaluate prediction accuracy (target RMSE < 10 %) and farmer satisfaction (≥ 80 % positive feedback).

## 5. Methodology
**Research Design:** Design Science Research.

**Phase 1 – Data Acquisition (Month 1):**
• Collect 5-year historical crop prices from UBOS & MAAIF.
• Gather rainfall/temperature data (NASA Power, UNMA).
• Scrape social-media posts or radio transcripts for sentiment signals using BeautifulSoup + VADER.

**Phase 2 – Model Development (Month 1-2):**
• Preprocess datasets (normalization, lag features).
• Implement models:
  o Baseline: Linear Regression, ARIMA.
  o Advanced: LSTM + Sentiment ensemble (PyTorch).
• Evaluate with train/test split and k-fold cross-validation.

**Phase 3 – Application & Voice Integration (Month 2-3):**
• Build prototype interface (Streamlit / Flask).
• Integrate Luganda voice using gTTS for forecasts (“Maize prices likely to rise tomorrow”).
• Optimize for offline caching of last 7 days’ predictions.

**Phase 4 – Field Testing (Month 3):**
• Pilot with 20 farmers in Wakiso & Masaka districts.
• Collect feedback via survey; adjust model and UI.

## 6. Expected Outcome
• Working AI tool providing 7-day price forecasts for major crops.
• Voice-enabled interface for low-literacy users.
• Reduced price-timing losses (goal ≥ 10 %).
• Open dataset and codebase for agricultural innovators.

## 7. Significance
Market Pulse empowers smallholders to plan sales strategically, increasing income stability and resilience. It supports Uganda’s Vision 2040 for modernized agriculture and SDGs 1 (No Poverty) & 2 (Zero Hunger). The platform can scale nationally through integration with NARO or mobile-network services.

## 8. Ethical and Practical Considerations
• Ensure farmer data privacy and informed consent.
• Communicate forecast uncertainty transparently (e.g., confidence levels).
• Avoid regional bias by sourcing diverse datasets.
• Prioritize women and low-literacy farmers in pilot participation.

## 9. Conclusion
In conclusion, Market Pulse seeks not just to inform farmers about current conditions, but to predict near-future prices, integrate market sentiment, and convert those forecasts into clear, actionable advice delivered in local languages. By doing so, it builds on the strengths of existing advisory services (like M-Omulimisa) while also focusing on the data-driven decision support in Uganda’s agricultural sector. This system promises direct economic impact empowering farmers to make better selling decisions.
