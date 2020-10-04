---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
price: €
allergens: 1,3,7
preview: /images/products/{{ .Name }}-thumb.jpg
images:
  - image: /images/products/{{ .Name }}.jpg
type: productos
weight: 1000
---
