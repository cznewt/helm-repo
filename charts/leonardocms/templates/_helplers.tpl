{{- define "leonardocms-fullname" -}}
{{- printf "leonardocms-%s" .Release.Name | trunc 55 | trimSuffix "-" -}}
{{- end -}}

