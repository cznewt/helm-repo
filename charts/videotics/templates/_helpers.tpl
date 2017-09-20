{{- define "videotics.fullname" -}}
{{- printf "videotics-%s" .Release.Name  | trunc 55 | trimSuffix "-" -}}
{{- end -}}

{{- define "videotics.kafka-address" -}}
    {{- if .Values.kafka.deployChart -}}
        {{- $ctx := . -}}
        {{- range $i, $e := until (int $.Values.kafka.replicas) -}}
            {{- if $i }},{{- end -}}
            {{- template "kafka-fullname" $ctx -}}
            {{- printf "-%d." $i -}}
            {{- template "kafka-fullname" $ctx -}}
            {{- printf ":%d" (int $.Values.kafka.port) -}}
        {{- end -}}
    {{- else -}}
        {{- printf "%s" .Values.kafka.externalAddress -}}
    {{- end -}}
{{- end -}}

{{- define "videotics.zk-address" -}}
    {{- if .Values.zookeeper.deployChart -}}
        {{- $ctx := . -}}
        {{- range $i, $e := until (int $.Values.zookeeper.replicas) -}}
            {{- if $i }},{{- end -}}
            {{- template "zk-fullname" $ctx -}}
            {{- printf "-%d." $i -}}
            {{- template "zk-fullname" $ctx -}}
            {{- printf ":%d" (int $.Values.zookeeper.clientPort) -}}
         {{- end -}}
    {{- else -}}
        {{- printf "%s" .Values.zookeeper.externalAddress -}}
    {{- end -}}
{{- end -}}

{{- define "videotics.spark-address" -}}
    {{- if .Values.spark.deployChart -}}
        {{- $ctx := . -}}
        {{- range $i, $e := until (int .Values.spark.spark.master.replicas) -}}
            {{- if $i }},{{- end -}}
            {{- template "master-fullname" $ctx -}}
            {{- printf "-%d:%d" $i (int $ctx.Values.spark.spark.master.rpcPort) -}}
        {{- end -}}
    {{- else -}}
        {{- printf "%s" .Values.spark.externalAddress -}}
    {{- end -}}
{{- end -}}

{{- define "videotics.hdfs-address" -}}
    {{- if .Values.hdfs.deployChart -}}
        {{- template "namenode-fullname" . -}}-0.{{- template "namenode-fullname" . -}}:{{ .Values.hdfs.namenode.port }}
    {{- else -}}
        {{- printf "%s" .Values.hdfs.externalAddress -}}
    {{- end -}}
{{- end -}}

{{- define "videotics.cassandra-address" -}}
    {{- if .Values.cassandra.deployChart -}}
        {{- printf "cassandra-%s" .Release.Name | trunc 55 | trimSuffix "-" -}}
    {{- else -}}
        {{- .Values.cassandra.externalAddress -}}
    {{- end -}}
{{- end -}}

{{- define "videotics-storage" -}}
    {{- if eq .Values.storage "hdfs" -}}
        {{- printf "hdfs://" -}}{{ template "videotics.hdfs-address" . }}{{- .Values.hdfs.path -}}
    {{- else -}}
        {{ template "videotics.cassandra-address" . }}:{{- .Values.cassandra.keyspace -}}:{{- .Values.cassandra.table -}}
    {{- end -}}
{{- end -}}
