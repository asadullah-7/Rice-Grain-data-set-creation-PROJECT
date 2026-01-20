import os
import numpy as np
import pandas as pd
from skimage import io, color, filters, morphology, measure, transform
import warnings

warnings.filterwarnings("ignore")

# ================= CONFIG =================
ROLL_NO = "L1F23BSCS0225"
REF_DIAMETER_MM = 30.0  
CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..")) 

OUT_DIR = os.path.join(BASE_DIR, "Grain_Images")
REJ_DIR = os.path.join(BASE_DIR, "Rejected")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(REJ_DIR, exist_ok=True)

rows = []
total_grain_counter = 1

all_folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]

varietyCounter = 0
for variety in all_folders:
    if variety.lower() in ["grain_images", "rejected", "code", ".git", ".ipynb_checkpoints"]:
        continue
    
    vpath = os.path.join(BASE_DIR, variety)
    img_list = sorted([f for f in os.listdir(vpath) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    
    if not img_list: continue
    varietyCounter += 1
    print(f"\n-> {varietyCounter} Variety: {variety}")

    for img_idx, img_name in enumerate(img_list, 1):
        img_path = os.path.join(vpath, img_name)
        
        try:
            img = io.imread(img_path)
            if img.ndim == 3 and img.shape[2] == 4: img = img[:, :, :3]
            
            gray = color.rgb2gray(img)
            thresh = filters.threshold_otsu(gray)
            binary = gray > thresh
            binary = morphology.remove_small_objects(binary, 300)
            binary = morphology.remove_small_holes(binary, 300)
            
            labels = measure.label(binary)
            regions = measure.regionprops(labels)
            
            if len(regions) < 2:
                io.imsave(os.path.join(REJ_DIR, img_name), img)
                continue

            # Reference Detection (Largest round object)
            regions = sorted(regions, key=lambda r: r.area, reverse=True)
            ref_obj = None
            for r in regions:
                if r.eccentricity < 0.85: 
                    ref_obj = r
                    break
            
            if not ref_obj:
                print(f"   !!! Reference cap not found in {img_name}")
                continue

            mm_per_pixel = REF_DIAMETER_MM / ref_obj.major_axis_length
            
            # Grains Processing
            for r in regions:
                if r.label == ref_obj.label: continue
                if r.area < 150 or r.area > 5000: continue # Filter boht baray ya boht chotay objects
                
                # Logic to make grain vertical
               
                angle = np.degrees(r.orientation)
                
                minr, minc, maxr, maxc = r.bbox
                m = 15 
                crop = img[max(0,minr-m):min(img.shape[0],maxr+m), 
                           max(0,minc-m):min(img.shape[1],maxc+m)]
                
               
                rotated = transform.rotate(crop, -angle, resize=True, preserve_range=True).astype(np.uint8)
                
               
                r_gray = color.rgb2gray(rotated)
                r_bin = r_gray > filters.threshold_otsu(r_gray)
                coords = np.argwhere(r_bin)
                if coords.size > 0:
                    y0, x0 = coords.min(axis=0); y1, x1 = coords.max(axis=0)
                    rotated = rotated[y0:y1, x0:x1]

                
                clean_variety = variety.replace(" ", "")
                g_name = f"{ROLL_NO}_{clean_variety}_Raw_{img_idx:03d}_Grain_{total_grain_counter:04d}.jpg"
                
                io.imsave(os.path.join(OUT_DIR, g_name), rotated)
                
                avg_c = np.mean(img[r.coords[:,0], r.coords[:,1]], axis=0)
                rows.append([g_name, variety, round(r.major_axis_length * mm_per_pixel, 2), 
                             round(r.minor_axis_length * mm_per_pixel, 2), 
                             int(avg_c[0]), int(avg_c[1]), int(avg_c[2])])
                total_grain_counter += 1
            
            print(f"   Processed {img_name}")

        except Exception as e:
            print(f"  !!! Error in {img_name}: {e}")

# Save CSV
if rows:
    df = pd.DataFrame(rows, columns=["Grain Image Name", "Variety Name", "Height (mm)", "Width (mm)", "Avg_R", "Avg_G", "Avg_B"])
    df.to_csv(os.path.join(BASE_DIR, "rice_metadata_final.csv"), index=False)
    print(f"\n DONE! Total Grains: {len(df)}")