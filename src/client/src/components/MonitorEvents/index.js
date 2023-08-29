import { useEffect, useState } from 'react';
import { Badge, Card, Stack, Table } from 'react-bootstrap';

import _ from 'lodash';
import { Link } from 'react-router-dom';
import moment from 'moment';
import { getEvents } from '../../http/api';

import styles from './styles/MonitorEvents.module.scss';
import Alert from '../Alert';
import useLocalStorage from '../../hooks/useLocalStorage';
import { useStore } from '../../Store/StoreProvider';

export default function MonitorEvents() {
  const { monitoring } = useStore();
  const [events, setEvents] = useState({
    items: [],
  });
  const [welcomeShown, setWelcomeShown] = useLocalStorage('welcome', true);

  const getData = async () => {
    const { content } = await getEvents({
      per_page: 50,
      page: 1,
    });
    setEvents(content);
  };

  useEffect(() => {
    getData().then(() => {});
  }, []);

  return (
    <Stack direction="vertical" gap={2}>
      <Stack direction="horizontal" gap={2}>
        <h5 className="mb-0">Events log</h5>
        <Card className="ms-auto" border="light" bg="light">
          <Card.Body>
            <Stack direction="horizontal" gap={2}>
              <span className="h5 mb-0">{monitoring.upMonitorsCount}</span>
              <Badge bg="success">UP</Badge>
            </Stack>
          </Card.Body>
        </Card>
        <Card border="light" bg="light">
          <Card.Body>
            <Stack direction="horizontal" gap={2}>
              <span className="h5 mb-0">{monitoring.downMonitorsCount}</span>
              <Badge bg="danger">DOWN</Badge>
            </Stack>
          </Card.Body>
        </Card>
        <Card border="light" bg="light">
          <Card.Body>
            <Stack direction="horizontal" gap={2}>
              <span className="h5 mb-0">{monitoring.pausedMonitorsCount}</span>
              <Badge bg="dark">PAUSE</Badge>
            </Stack>
          </Card.Body>
        </Card>
      </Stack>
      <Table bsPrefix={styles.table}>
        <thead>
          <tr>
            <th>monitor</th>
            <th>event</th>
            <th>reason</th>
            <th>datetime</th>
          </tr>
        </thead>
        <tbody>
          {events.items.map((event) => {
            const datetime = moment
              .utc(event.datetime)
              .local()
              .format('YYYY-MM-DD HH:mm:ss');

            return (
              <tr key={event.id}>
                <td className={styles.monitorLinkCell}>
                  <Link
                    to={`/monitoring/${event.monitor_id}`}
                    className={styles.monitorLink}
                  >
                    {event.monitor_id}
                  </Link>
                </td>
                <td>
                  <span
                    className={`bg-transparent fw-bold small text-${
                      event.event === 'UP' ? 'success' : 'danger'
                    }`}
                  >
                    {event.event}
                  </span>
                </td>
                <td>{_.startCase(_.lowerCase(event.reason))}</td>
                <td>{datetime}</td>
              </tr>
            );
          })}
          {events.items.length === 0 && (
            <tr>
              <td colSpan="4">log is empty, nothing has happened 🤗</td>
            </tr>
          )}
        </tbody>
      </Table>
      <Alert
        defaultShown={welcomeShown}
        onExited={() => setWelcomeShown(false)}
      >
        <p>
          Hey! Here you can see a summary of the events that have occurred with
          your resources recently.
        </p>
        <p>For now, log is empty. To get started, create your first monitor!</p>
      </Alert>
    </Stack>
  );
}
