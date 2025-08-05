# CulturalPragmatics

This repo contains data under a unified Concept (X) + culture (C) -> Value (y). 

We have following concepts:
- Time expression: [unified/time_expressions.csv](unified/time_expressions.csv)
- Gradable adjectives: [unified/gradable_adjectives.csv](unified/gradable_adjectives.csv)
- Quantifier: [unified/quantifier.csv](unified/quantifier.csv)
- Missing_head_noun: [unified/metrics.csv](unified/metrics.csv)

| idx | Concept            | Value Type         | Example                   | Cultures/Languages        | # of Instances                   | Readiness      | Collected in Ori Lang or English?       |
|-----|--------------------|--------------------|---------------------------|---------------------------|-----------------------------------|---------------|----------------------------------------|
| 1   | Time expression    | Range              | Morning → (8AM, 12PM)     | EN, HI, IT, PT            | 4 cultures × 5 expressions        | ✅ Git Link    | EN (but allowed native substitution)   |
| 2   | Gradable adjectives| Ranking            | dim < gloomy              | EN, FR, ES, EL            | 433 lists of adjectives           | ✅ Git Link    | Original LANG native speakers          |
| 3   | Quantifiers        | Range              | Some → (0, 0.5)           | EN, FR, SL, DE            | 4 languages × 5 quantifiers       | ✅ Git Link    | Native                                 |
| 4   | Missing head noun  | Categorical mapping| He paid me 180 __         | US, CN, CA, EU, SG, …     | World knowledge collected by ourselves | ✅ Git Link    | / (synthesized world knowledge)        |
| 5   | Dollar Street (multimodal) | An image (house utility domain) | "Stove" at JP is 🥣 | Wide coverage | 40k+ images | ✅ Git Link | NA |
| 6   | CROCUFID (multimodal) | A score based on the image (food domain) | 🍗 at JP is 100% delicious | US, UK, Japan | 840 images | ✅ Git Link | Native language |
