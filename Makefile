############################################
-include Makefile.options
############################################
url?=https://mozilla-common-voice-datasets.s3.dualstack.us-west-2.amazonaws.com/cv-corpus-12.0-2022-12-07/cv-corpus-12.0-2022-12-07-lt.tar.gz
data_dir?=data
gz?=cv-corpus-12.0-2022-12-07-lt.tar.gz
python_cmd=PYTHONPATH=./ LOG_LEVEL=INFO python
work_dir?=work
extr_dir?=cv-corpus-12.0-2022-12-07/lt
n?=20
############################################
${work_dir}/extracted: 
	mkdir -p $@
${data_dir}:
	mkdir -p $@	
############################################
${work_dir}/extracted/.done: $(data_dir)/${gz} | ${work_dir}/extracted
	tar xvzf $(data_dir)/${gz} -C ${work_dir}/extracted
	touch $@
############################################
${data_dir}/${gz}: | ${data_dir}
	curl ${url} -o $@_
	mv $@_ $@
############################################
${work_dir}/ref.txt: ${work_dir}/extracted/.done
	cat ${work_dir}/extracted/${extr_dir}/test.tsv | cut -f 2,3 | tail -n +2 > $@
############################################
${work_dir}/predicted.txt: ${work_dir}/ref.txt
	$(python_cmd) src/predict.py --in_f $^ --l ${work_dir}/extracted/${extr_dir}/clips > $@_
	mv $@_ $@
############################################
eval/wer: ${work_dir}/predicted.txt ${work_dir}/ref.txt
	$(python_cmd) src/estimate.py --ref ${work_dir}/ref.txt --pred ${work_dir}/predicted.txt
.PHONY: eval/wer
############################################
eval/cmp: ${work_dir}/predicted.txt ${work_dir}/ref.txt
	$(python_cmd) src/cmp.py --ref ${work_dir}/ref.txt --pred ${work_dir}/predicted.txt --n $(n)
.PHONY: eval/cmp
############################################
clean:
	rm -rf $(work_dir)
clean/data:
	rm -rf $(data_dir)
.PHONY: clean

