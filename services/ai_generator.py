import replicate
import os

def generate_video(prompt):
    output = replicate.run("another-ai-studio/zeroscope-v2-xl",
                        input={"prompt": prompt,
                               "motion_bucket_id": 40, 
                               "frames":16})
    return output
    
    