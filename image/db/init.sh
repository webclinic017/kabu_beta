#!/bin/sh

if [ -f /tmp/kabu_beta.sql ]; then
  mysql -udbuser -pdbpass kabu < /tmp/kabu_beta.sql
fi

