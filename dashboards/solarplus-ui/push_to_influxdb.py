def push_to_influx_database(
    self, data: DataFrame, measurement: str
) -> None:
    """
    Push dataframe to database.
    :param data: pandas DataFrame indexed by timestamp
    :param measurement: the name of this measurement
    :return:
    """
    def preprocess_data(data_: DataFrame) -> DataFrame:
        """
        :param data_: the original data
        :return: data in the desired format
        """
        columns = list(data_.columns)

        # for influx, ts must in datetime format
        data_['ts'] = DatetimeIndex(data_['ts'].apply(
            # "YYYY-MM-DD HH:MM:SS"
            lambda ts: to_datetime(
                arg=ts, format='%Y%m%d%H%M%S'
            )
        ))

        # swap to ensure that ts is the first column
        ts_index: int = columns.index('ts')
        columns[0], columns[ts_index] = columns[ts_index], columns[0]
        data_ = data_[columns]

        return data_

    def data_chunks(data_: DataFrame) -> Generator[DataFrame, None, None]:
        """
        It's necessary to break up the data into multiple chunks.
        Each chunk will be written separately.
        :param data_: original data
        :return: a generator for the chunks
        """
        row_count: int = data_.shape[0]

        # keep track of which chunk each row belongs to.
        # a series of repeated -1's.
        chunk_numbers: Series = Series([-1] * row_count)

        # keep track of unique timestamps we find
        repeats_per_ts: Dict[datetime, int] = {}

        for i, row in data_.iterrows():

            ts: datetime = row['ts']

            # ensure that there's an entry for ts
            if ts not in repeats_per_ts:
                repeats_per_ts[ts] = -1

            # Record that this we've seen this timestamp n times.
            repeats_per_ts[ts] = repeats_per_ts[ts] + 1

            # this row's chunk_number = n
            chunk_numbers[i] = repeats_per_ts[ts]

        last_chunk_number: int = max(repeats_per_ts.values())

        for chunk_n in range(0, last_chunk_number+1):
            chunk = data_.loc[
                # return the rows whose chunk_number matches chunk_n
                chunk_numbers == chunk_n
            ].copy()

            chunk.set_index('ts', inplace=True)

            yield chunk


    data: DataFrame = preprocess_data(data)

    for chunk in data_chunks(data):
        self.influx_client.write_points(
            dataframe=chunk,
            measurement=measurement,
            database=self.database,
            tag_columns=['id']
        )
