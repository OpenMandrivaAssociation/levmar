#!/bin/sh
curl -L "https://users.ics.forth.gr/~lourakis/levmar/" 2>/dev/null |grep "Latest:" |sed -ne 's,.*>levmar-\(.*\)<\/a.*,\1,p'

