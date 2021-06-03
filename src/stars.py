import glob
import json
import pandas as pd
from pathlib import Path

paths = glob.glob('data/*.json')
rows = []
for file_path in paths:
	with open(file_path, encoding="utf-8") as file:
		reviews = json.load(file)
		for review in reviews:
			factors = review['factors']
			factory_types = list(factors.keys())
			p = Path(file_path).relative_to(root)
			row = {
				'employer': p.with_suffix('')
			}
			for factor_type in factory_types:
				factor_stars = factors[factor_type]['score']
				if factor_stars:
					row[factor_type] = float(factor_stars)
			rows.append(row)
df = pd.DataFrame(rows)
writer = pd.ExcelWriter('./result/stars.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()
