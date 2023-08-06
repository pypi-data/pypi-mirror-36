Qth Postgres Log
================

A logging service for [Qth](https://github.com/mossblaser/qth) which stores Qth
events and properties into a PostgreSQL database.


Usage
-----

Just run:

    $ qth_postgres_log

Which will create and start populating tables `qth_log` and `qth_paths` in the
database and username matching the current system username.


Tables
------

All Qth events are logged into the `qth_log` table with paths being recorded in
`qth_paths`.

The `qth_log` table has the following columns:

* `log_id`: Unique ID.
* `path_id`: Foreign key referencing `qth_paths.path_id`. The path this log
  item corresponds to.
* `value`: Value (JSONB). `NULL` if an invalid JSON or the value was deleted.
* `time`: Timestamp at which the value was received.

The `qth_path` table has the following columns.

* `path_id`: A unique ID.
* `path`: The TEXT containing the Qth path.

For convenience, a function `qth_path_to_id` is provided which takes a Qth path
(as TEXT) and returns its ID, creating it if not already present in that table.


HTTP Query API
--------------

In addition to querying the Postgres database directly, Qth Postgres Log also
provides a basic HTTP API for carrying out simple lookups of historical values.
The URL at which the API is being served is advertised in the Qth property
`sys/log/api-url`.

The advertised URL can be overridden using `--http-api-url` (e.g. if the API is
behind a reverse proxy). The serving host and port can also be changed and the
API can also be disabled entirely, see `--help`.

The following endpoint is currently provided:

### `{api-url}/value`

This endpoint returns historical values of a single Qth entity in JSON format
in response to HTTP GET requests.

The returned JSON response will contain an array of `{"value": ..., "time":
...}` objects. The value field contains the value of the entity at the
specified time unless the entity was deleted in which case the field will be
omitted. The time field gives the time at which the value was recorded.
Generally this will be a UTC ISO 8601-style timestamp string (i.e.
"yyyy-mm-ddThh:mm:ss") unless otherwise noted below.

The endpoint is controlled by query parameters appended to the URL as follows.

#### `path=<qth path>`

**Mandatory.** Specifies the Qth path to lookup. Wildcards are not supported.

#### `limit=<integer>`

Optional. Limit the number of entries returned to at most this number. Set to
'0' to remove limit. Default is 100.

#### `start=<yyyy-mm-ddThh:mm:ss>` and  `end=<yyyy-mm-ddThh:mm:ss>`

Optional. Limit the date range of log entries to include. By default, no limit
is applied. Timestamps should be formatted as shown above and be in UTC.

#### `index=<index specification>`

Optional. If the logged values contain JSON objects or arrays, a particular
element or entry can be returned in place of the whole object or array.

If values contain arrays such as `[10, 20, 30, 40]`, setting `index=0` will
extract the first element in every array (i.e. `10` in the example).

Negative indices access elements indexed from the end of the array, e.g.
`index=-1` will extract `40` from the previous example.

If values contain objects such as `{"foo": 123, "bar": 321}`, setting
`index="bar"` will extract the "bar" entry in every array (i.e. `321` in the
example). Note the double quotes around the object key.

Values can also be indexed from deeply nested structures by seperating several
indices and object keys with commas. For example, `{"foo": [10, 20, 30, 40]}`
might be indexed with `index="foo",0` resulting in `10` being selected.

If an index is invalid for a value (e.g. if the value is of the wrong type or
index or object key does not exist), the value will be returned as if deleted
(i.e. the "value" field will be omitted from the returned log entry).

#### `empty=<1 or 0>`

Optional. Should empty values (e.g. deleted values or values which couldn't be
indexed by the `index` option) be included in results. Defaults to 1 (include
empty values).

#### `order=<time, value, -time, -value>`

Optional. Specify how entries are ordered in the returned JSON. Defaults to
time.

If 'time', the most recent values are listed first.

If 'value', the values with the largest value are listed first.

The '-' prefixed versions of the above use the reverse ordering.


#### `window=<minute, hour, day, week, month, quarter, year>`

Optional. If specified, log entries are grouped together at the specified
granularity and an aggragated value is returned (see `aggregate`). This can be
used to reduce large quantites of historical data to a more manageable form or
to produce simple histograms of discrete event frequencies over time.

Do not use at the same times as `group`.

#### `group=<minute, hour, day, dow, week, month, quarter, year>`

Optional. If specified, log entries are grouped together by the named time
component and aggregate values are returned (see `aggregate`). The 'time' field
in the returned results will be set to an integer (rather than an ISO 8601
style string).

This option allows, for example, daily, weekly or annual trends to be
identified.

By contrast with the `window` option, using `group` aggregates *all* records
with a common date/time element together, not just those in the same block of
time. For example, `group=hour` will group together all log entries between
00:00:00 and 00:59:59 each day into a single row in the output whose 'time'
field will be 0, and all entries between 01:00:00 and 01:59:59 into another row
with 'time' 1 and so on.

Do not use at the same times as `window`.

#### `aggregate=<count, avg, min, max>`

Optional. When `window` or `group` are used, specifies the aggregation method
to use for returned values. The default is `avg`.

* `count` returns the number of aggregated entries (excluding empty entries if
  `empty=0` is used).
* `avg` returns the mean value of aggragated entries.
* `min` returns the minimum value of aggragated entries.
* `max` returns the maximum value of aggragated entries.

Before aggregation, JSON values are cast to floats as follows:

* Numbers are cast as-is
* The following are cast to 1.0:
    * `true`
    * Non-empty arrays
    * Non-empty objects
    * Non-empty strings
* The following are cast to 0.0:
    * `false`
    * `null`
    * Empty arrays
    * Empty objects
    * Empty strings
    * Empty (i.e. deleted) values

If `index` is used, the indexed values are aggregated.
