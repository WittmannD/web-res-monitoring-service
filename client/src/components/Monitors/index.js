import ListGroup from 'react-bootstrap/ListGroup';
import React, { useEffect, useState } from 'react';
import { observer } from 'mobx-react-lite';
import moment from 'moment';
import { useNavigate, useParams } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';
import { Button, Stack } from 'react-bootstrap';

import { useStore } from '../../Store/StoreProvider';
import { getMonitors } from '../../http/api';
import { modalOptions } from '../Modals/CreationModal';
import Alert from '../Alert';

const badgeColors = {
  UP: 'success',
  DOWN: 'danger',
  PAUSE: 'dark',
};

function Monitors() {
  const [alertShown, setAlertShown] = useState(false);
  const { monitoring, modals } = useStore();
  const navigate = useNavigate();
  const params = useParams();

  useEffect(() => {
    getMonitors()
      .then((data) => {
        monitoring.setMonitors(data.content.items);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }, []);

  const toMonitor = (monitorId) =>
    navigate(`/dashboard/${monitorId}`, { replace: true });

  const newMonitorAvailable = monitoring.activeMonitorsCount < 3;

  const onAdd = () => {
    if (!newMonitorAvailable) {
      setAlertShown(true);
    } else {
      modals.createModal(modalOptions());
    }
  };

  return (
    <Stack direction="vertical" gap={2}>
      <Stack direction="horizontal" gap={2}>
        <Stack
          as={Button}
          onClick={onAdd}
          direction="horizontal"
          size="sm"
          gap={1}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
              clipRule="evenodd"
            />
          </svg>
          Add New Monitor
        </Stack>
      </Stack>
      <Alert
        variant="danger"
        in={alertShown && !newMonitorAvailable}
        defaultShown={alertShown}
        onClose={() => setAlertShown(false)}
      >
        <p>You can only have 3 active monitors. Pause one to create another.</p>
      </Alert>
      <ListGroup as="ul" role="list">
        {monitoring.monitors.map((monitor, i) => {
          const nextCheckAt = moment
            .utc(monitor.next_check_at)
            .local()
            .fromNow();
          const active =
            params.monitorId && Number(params.monitorId) === monitor.id;
          const status = !monitor.running ? 'PAUSE' : monitor.status;

          return (
            <ListGroup.Item
              action
              role="listitem"
              key={monitor.id}
              disabled={active}
              onClick={() => toMonitor(monitor.id)}
            >
              <Stack direction="horizontal">
                <span className="me-auto text-muted">
                  {monitor.running ? `next check ${nextCheckAt}` : '-'}
                </span>
                <Badge bg={badgeColors[status]}>{status}</Badge>
              </Stack>
              <div className="fw-bold">{monitor.url}</div>
            </ListGroup.Item>
          );
        })}
        {monitoring.monitors.length === 0 && (
          <ListGroup.Item role="listitem">
            Nothing here. Create monitor for start.
          </ListGroup.Item>
        )}
      </ListGroup>
      <Alert variant="secondary" closable={false} appear={false}>
        <p>
          This application created for simple development purposes. For more
          features, try to use a more{' '}
          <a
            href="https://uptimerobot.com/?rid=57a2299170af03"
            target="_blank"
            rel="nofollow noopener noreferrer"
          >
            advanced monitoring system
          </a>
          .
        </p>
      </Alert>
    </Stack>
  );
}

export default observer(Monitors);
