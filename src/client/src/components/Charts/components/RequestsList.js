import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Stack, Table } from 'react-bootstrap';
import moment from 'moment';
import { getMonitorRequests } from '../../../http/api';

import styles from '../styles/RequestsList.module.scss';
import Paging from '../../Paging';
import RequestsListPlaceholder from './RequestsListPlaceholder';

export default function RequestsList() {
  const [isLoading, setIsLoading] = useState(true);
  const [requests, setRequests] = useState({});
  const { monitorId } = useParams();

  const getData = async (pageNumber) => {
    const { content } = await getMonitorRequests(monitorId, {
      per_page: 10,
      page: pageNumber,
    });
    setRequests(content);
  };

  const onPageChange = (pageNumber) => {
    getData(pageNumber).then(() => setIsLoading(false));
  };

  useEffect(() => {
    getData(1).then(() => setIsLoading(false));

    return () => {
      setIsLoading(true);
    };
  }, []);

  return !isLoading ? (
    <Stack direction="vertical" gap={2}>
      <Table bsPrefix={styles.table}>
        <thead>
          <tr>
            <th>status</th>
            <th>elapsed</th>
            <th>datetime</th>
          </tr>
        </thead>
        <tbody>
          {requests.items.map((request) => {
            const preparedDateTime = moment
              .utc(request.timestamp)
              .local()
              .format('YYYY-MM-DD HH:mm');

            return (
              <tr key={request.id}>
                <td>{request.status_code}</td>
                <td>{request.elapsed}</td>
                <td>{preparedDateTime}</td>
                <td>
                  <a href="">details</a>
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
      <Paging
        activePage={requests.page}
        totalPages={requests.pages}
        onPageChange={onPageChange}
      />
    </Stack>
  ) : (
    <RequestsListPlaceholder />
  );
}
