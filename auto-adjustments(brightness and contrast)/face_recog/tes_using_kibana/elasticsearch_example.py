from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch()

with open('./2010_Census_Populations_by_Zip_Code.csv') as f:
  index_name = 'census_data_records'
  doctype = 'census_record'
  reader = csv.reader(f)
  headers = []
  index = 0
  es.indices.delete(index=index_name, ignore=[400, 404])
  es.indices.create(index=index_name, ignore=400)
  es.indices.put_mapping(
      index=index_name,
      doc_type=doctype,
      ignore=400,
      body={
          doctype: {
              "properties": {
                  "Zip Code": {
                      "type": "float"
                      },
                  "Total Population": {
                      "type": "float",
                  },
                  "Median Age": {
                      "type": "float"
                  },
                  "Total Males": {
                      "type": "float",
                  },
                  "Total Females": {
                      "type": "float",
                  },
                  "Total Households": {
                      "type": "float",
                  },
                  "Average Household Size": {
                      "type" :"float"
                  }
              }
          }
      }
  )
  for row in reader:
      try:
          if(index == 0):
              headers = row
          else:
              obj = {}
              for i, val in enumerate(row):
                  obj[headers[i]] = float(val)
              print(obj)
              # put document into elastic search
              es.index(index=index_name, doc_type=doctype, body=obj)
              print(obj)

      except Exception as e:
          print('error: ' + str(e) + ' in' + str(index))
      index = index + 1

f.close()