############################################
-include Makefile.options
############################################
data_dir?=data
python_cmd=PYTHONPATH=./ LOG_LEVEL=INFO python
work_dir?=work
n?=20
tr_url?=https://atpazinimas.intelektika.lt
############################################
common_voice_gz?=cv-corpus-24.0-2025-12-05-lt.tar.gz
extr_dir?=cv-corpus-24.0-2025-12-05/lt
############################################
${work_dir}/extracted: 
	mkdir -p $@
${data_dir} ${work_dir}/cache:
	mkdir -p $@	
############################################
${data_dir}/${common_voice_gz}: | ${data_dir}
	echo "Manually Download Common Voice LT test corpus to ${data_dir}/${common_voice_gz}"
	exit 1	
${work_dir}/extracted/.done: ${data_dir}/${common_voice_gz} | ${work_dir}/extracted
	tar xvzf ${data_dir}/${common_voice_gz} -C ${work_dir}/extracted
	touch $@
############################################
${work_dir}/ref.txt: ${work_dir}/extracted/.done
	cat ${work_dir}/extracted/${extr_dir}/test.tsv | cut -f 2,4 | tail -n +2 > $@
############################################
${work_dir}/predicted.txt: ${work_dir}/ref.txt | ${work_dir}/cache
	$(python_cmd) src/predict.py --in_f $^ --l ${work_dir}/extracted/${extr_dir}/clips \
		--cache_dir ${work_dir}/cache --url $(tr_url) > $@_
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
eval/tmp/wer: ${work_dir}/ref.txt
	$(python_cmd) src/estimate.py --ref ${work_dir}/ref.txt --pred ${work_dir}/predicted.txt_ 
.PHONY: eval/tmp/wer
############################################
clean:
	rm -rf $(work_dir)
clean/data:
	rm -rf $(data_dir)
.PHONY: clean

