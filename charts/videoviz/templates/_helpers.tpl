{{- define "fullname" -}}
{{- printf "videoviz-%s" .Release.Name  | trunc 55 | trimSuffix "-" -}}
{{- end -}}
