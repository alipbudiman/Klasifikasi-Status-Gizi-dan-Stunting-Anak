import pandas as pd

class ReadTabel:
    def __init__(self) -> None:
        pass
    
    def check_gender(self, gender):
        if gender.lower() == "l":
            file_path = "rule_l.csv"
            file_path2 = "rule2_l.csv"
            return file_path, file_path2
        elif gender.lower() == "p":
            file_path = "rule_p.csv"
            file_path2 = "rule2_p.csv"
            return file_path, file_path2
        else:
            raise Exception("gender input must l for male (laki-laki) or p for female (perempuan)")
    
    def load_rules(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = ['USIA', '-SD 3', '-SD 2', '-SD 1', 'Median', '+SD 1', '+SD 2', '+SD 3']
        df['USIA'] = pd.to_numeric(df['USIA'], errors='coerce')  # Ubah ke numerik untuk kolom 'USIA'
        return df


    def find_closest_age(self, age, rules_df):
        closest_age = rules_df.iloc[(rules_df['USIA'] - age).abs().argmin()]
        return closest_age

    def stunting_status_by_age_height(self, age, height, rules_df):
        closest_age_row = self.find_closest_age(age, rules_df)        
        try:
            sd_3 = closest_age_row['-SD 3']
            sd_2 = closest_age_row['-SD 2']
            sd_0 = closest_age_row['Median']
            sd_3_plus = closest_age_row['+SD 3']
        except KeyError as e:
            raise KeyError(f"Kolom yang diperlukan tidak ditemukan: {e}")

        if height < sd_3:
            return 1, "Sangat Pendek"
        elif sd_3 <= height < sd_2:
            return 0.8 , "Pendek"
        elif sd_2 <= height <= sd_3_plus:
            return 0.6,  "Normal"
        else:
            return 0.4, "Tinggi"

    def load_rules2(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = ['Panjang Badan (cm)', '-3 SD', '-2 SD', '-1 SD', 'Median', '+1 SD', '+2 SD', '+3 SD']
        
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Ubah ke numerik, coerce ubah error jadi NaN
        
        return df

    def find_closest_height2(self, height, rules_df):
        rules_df['Panjang Badan (cm)'] = pd.to_numeric(rules_df['Panjang Badan (cm)'], errors='coerce')
        closest_row = rules_df.iloc[(rules_df['Panjang Badan (cm)'] - height).abs().argmin()]
        return closest_row

    def stunting_weight_by_height(self, height, weight, rules_df):
        closest_row = self.find_closest_height2(height, rules_df)
        
        sd_3_minus = closest_row['-3 SD']
        sd_2_minus = closest_row['-2 SD']
        sd_1_plus = closest_row['+1 SD']
        sd_2_plus = closest_row['+2 SD']
        sd_3_plus = closest_row['+3 SD']

        if weight < sd_3_minus:
            return 1, "Gizi Buruk"
        elif sd_3_minus <= weight < sd_2_minus:
            return 0.8, "Gizi Kurang"
        elif sd_2_minus <= weight <= sd_1_plus:
            return 0.6, "Gizi Baik"
        elif sd_1_plus < weight <= sd_2_plus:
            return 0.4, "Berisiko Gizi Lebih"
        elif sd_2_plus < weight <= sd_3_plus:
            return 0.2, "Gizi Lebih"
        else:
            return 0.8,  "Obesitas"


# pembuatan instance class ReadTable
rt = ReadTabel()


# contoh data anak
jenis_kelamin = "l" # l untuk laki-laki
umur = 10 # umur 10 bulan
panjang_badan_atau_tinggi_banad = 8
berat_badan = 9.2 # dalam skala kg


# menentukan tingkat stunting menurut tinggi badan
# dari data panjang badan atau tinggi badan menurut umur
# (PB/U atau TB/U) anak usia 0-60 bulan
 
rule_df1, _ = rt.check_gender(jenis_kelamin)
rules_data = rt.load_rules(rule_df1)
nilai, status = rt.stunting_status_by_age_height(umur, panjang_badan_atau_tinggi_banad, rules_data)
print("Nilai kemungkinan anak mengalami stunting dari panjang atau tinggi badan:", nilai)
print("Status anak", status)


# menentukan tingkat stunting 
# dengan data berat badan menurut tinggi badan
# (BB/PB atau BB/TB) anak usia - 60

_, rule_df2 = rt.check_gender(jenis_kelamin)
rules_data2 = rt.load_rules2(rule_df2)
nilai, status = rt.stunting_weight_by_height(panjang_badan_atau_tinggi_banad, berat_badan, rules_data2)
print("Nilai kemungkinan anak mengalami stunting dari panjang atau tinggi badan:", nilai)
print("Status anak", status)