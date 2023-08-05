AVRO-GEN-TOPKRABBENSTEAM
=========================
##### Avro record class and specific record reader generator.

Based on the original github project https://github.com/rbystrit/avro_gen, this one was forked in order to fix a problem related to load this library in a docker container. Problem was solved by rewriting tiny bit of a code, which generates "schema.avsc" file.
Loading this file in a docker container was a problem, so we decided to store "schema.avsc" file internally inside schema_classes.py file as a string.
The same approach is used by avrogen library developed for .Net Core AvroGen.
 
##### Usage:
		import json
		import io
		with open("schema.json",'r') as file:            
			schema_json = file.read()
			output_directory = "SchemaDir"
			from avrogen import write_schema_files
			write_schema_files(schema_json, output_directory)
    
=========================
##### This fork is dedicated to Alex (stack tsar, chapter lead) and Iskander (King).
=========================
 



    