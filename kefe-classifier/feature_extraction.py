"""
The feature extraction tool
"""
import argparse
import subprocess
import csv
import os
from pathlib import Path

bert_path = 'bert-master'
# phrase_file = 'temp/candidate_phrase.tsv'
phrase_file = 'temp'
temp_dir = 'temp'
Path(temp_dir).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Extract features from the given app description.')
  parser.add_argument('-o', metavar='OUTPUT_FILE', type=str, default='features.txt',
                      help='the file of features extracted (default: features.txt)')
  parser.add_argument('--bert', type=str, default=bert_path,
                      help='path of bert directory (default: {})'.format(bert_path))
  
  args = parser.parse_args()
  output_file = args.o
  bert_path = args.bert = args.bert
  
  print('[INFO] candidate phrases extracted: {}'.format(phrase_file))

  subprocess.run('python3 {}/run_classifier.py'
                ' --task_name=extract'
                ' --do_train=true'
                ' --do_predict=true'
                ' --data_dir={}'
                ' --vocab_file={}/uncased_L-12_H-768_A-12/vocab.txt'
                ' --bert_config_file={}/uncased_L-12_H-768_A-12/bert_config.json'
                ' --init_checkpoint={}/uncased_L-12_H-768_A-12/bert_model.ckpt'
                ' --max_seq_length=128'
                ' --output_dir={}'.format(bert_path, phrase_file, bert_path, bert_path, bert_path, temp_dir),
                shell=True)
  
  # os.remove(temp_dir + '/predict.tf_record')
  print('[INFO] prediction result of classifier: {}/test_results.tsv'.format(temp_dir))
  
  # get the final feature describing phrases
  candidate_phrase = []
  with open(phrase_file, encoding='utf-8') as file:
    for row in csv.reader(file, delimiter='\t'):
      candidate_phrase.append(row[1])
  print(len(candidate_phrase))

  writer = open(output_file, 'w', encoding='utf-8')
  with open(temp_dir + '/test_results.tsv', encoding='utf-8') as file:
    index = 0
    for row in csv.reader(file, delimiter='\t'):
      p1, p2 = float(row[0]), float(row[1])   # labels 1 and 2
      # print(p1,p2)
      if p1 > p2:
        writer.write(candidate_phrase[index])
        writer.write('\n')
      index += 1
    print(index)
  writer.close()
  print('[INFO] the set of features: {}'.format(output_file))
  print('[TASK FINISHED]')
