# src/ai/export_csv.py
import csv
import os




def export_training_data(features_list, labels_list, feature_names, output_path='src/ai/training_data.csv'):
    """
    Записва training dataset във CSV формат.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(feature_names + ['label'])
        for feats, label in zip(features_list, labels_list):
            writer.writerow(feats + [label])
    print(f"📁 Тренировъчните данни са експортирани в {output_path}")
