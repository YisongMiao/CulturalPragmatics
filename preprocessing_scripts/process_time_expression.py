import json
from collections import defaultdict
import os


if __name__ == "__main__":
    with open("unified/raw_data/time_expression.jsonl", "r") as f:

        stored_data = defaultdict(lambda: defaultdict(dict))

        for line in f:
            data = json.loads(line)
            country = data["country"]
            languages = data["languages"]
            main = data["main"]
            additional_times = data["additional_times"]


            if "morning" in main:
                morning_start_mean = main["morning"]["start_mean"]
                morning_start_std = main["morning"]["start_std"] 
                morning_end_mean = main["morning"]["end_mean"]
                morning_end_std = main["morning"]["end_std"]
                stored_data[country]['morning']["start_mean"] = morning_start_mean
                stored_data[country]['morning']["start_std"] = morning_start_std
                stored_data[country]['morning']["end_mean"] = morning_end_mean
                stored_data[country]['morning']["end_std"] = morning_end_std
                
            if "noon" in main:
                noon_start_mean = main["noon"]["start_mean"]
                noon_start_std = main["noon"]["start_std"]
                noon_end_mean = main["noon"]["end_mean"] 
                noon_end_std = main["noon"]["end_std"]
                stored_data[country]['noon']["start_mean"] = noon_start_mean
                stored_data[country]['noon']["start_std"] = noon_start_std
                stored_data[country]['noon']["end_mean"] = noon_end_mean
                stored_data[country]['noon']["end_std"] = noon_end_std

            if "afternoon" in main:
                afternoon_start_mean = main["afternoon"]["start_mean"]
                afternoon_start_std = main["afternoon"]["start_std"]
                afternoon_end_mean = main["afternoon"]["end_mean"]
                afternoon_end_std = main["afternoon"]["end_std"]
                stored_data[country]['afternoon']["start_mean"] = afternoon_start_mean
                stored_data[country]['afternoon']["start_std"] = afternoon_start_std
                stored_data[country]['afternoon']["end_mean"] = afternoon_end_mean
                stored_data[country]['afternoon']["end_std"] = afternoon_end_std

            if "evening" in main:
                evening_start_mean = main["evening"]["start_mean"]
                evening_start_std = main["evening"]["start_std"]
                evening_end_mean = main["evening"]["end_mean"]
                evening_end_std = main["evening"]["end_std"]
                stored_data[country]['evening']["start_mean"] = evening_start_mean
                stored_data[country]['evening']["start_std"] = evening_start_std
                stored_data[country]['evening']["end_mean"] = evening_end_mean
                stored_data[country]['evening']["end_std"] = evening_end_std

            if "night" in main:
                night_start_mean = main["night"]["start_mean"]
                night_start_std = main["night"]["start_std"]
                night_end_mean = main["night"]["end_mean"]
                night_end_std = main["night"]["end_std"]
                stored_data[country]['night']["start_mean"] = night_start_mean
                stored_data[country]['night']["start_std"] = night_start_std
                stored_data[country]['night']["end_mean"] = night_end_mean
                stored_data[country]['night']["end_std"] = night_end_std
            
            print(country)
            print(morning_start_mean, morning_start_std, morning_end_mean, morning_end_std)
            print(noon_start_mean, noon_start_std, noon_end_mean, noon_end_std)
            print(afternoon_start_mean, afternoon_start_std, afternoon_end_mean, afternoon_end_std)
            print(evening_start_mean, evening_start_std, evening_end_mean, evening_end_std)
            print(night_start_mean, night_start_std, night_end_mean, night_end_std)

        
        
            # Write header if file doesn't exist
            if not os.path.exists('unified/time_expressions.csv'):
                with open('unified/time_expressions.csv', 'w') as f:
                    f.write("Country,Concept,Start_Mean,Start_Std,End_Mean,End_Std\n")

            with open('unified/time_expressions.csv', 'a') as f:
                # Morning row
                f.write(f"{country},Morning,{morning_start_mean},{morning_start_std},{morning_end_mean},{morning_end_std}\n")
                
                # Noon row
                f.write(f"{country},Noon,{noon_start_mean},{noon_start_std},{noon_end_mean},{noon_end_std}\n")
                
                # Afternoon row 
                f.write(f"{country},Afternoon,{afternoon_start_mean},{afternoon_start_std},{afternoon_end_mean},{afternoon_end_std}\n")
                
                # Evening row
                f.write(f"{country},Evening,{evening_start_mean},{evening_start_std},{evening_end_mean},{evening_end_std}\n")
                
                # Night row
                f.write(f"{country},Night,{night_start_mean},{night_start_std},{night_end_mean},{night_end_std}\n")