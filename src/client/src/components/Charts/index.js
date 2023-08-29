import { Button, Stack, Tab } from 'react-bootstrap';
import PropTypes from 'prop-types';
import AreaChart from './components/AreaChart';
import RequestsList from './components/RequestsList';

export default function Charts({ activeTab, setActiveTab }) {
  return (
    <Stack gap={3} className="mt-3">
      <Tab.Container activeKey={activeTab} unmountOnExit>
        <Stack direction="horizontal" gap={2}>
          <Button variant="light" onClick={() => setActiveTab('chart')}>
            Chart
          </Button>
          <Button variant="light" onClick={() => setActiveTab('list')}>
            Requests List
          </Button>
        </Stack>
        <Tab.Content>
          <Tab.Pane eventKey="chart">
            <AreaChart />
          </Tab.Pane>
          <Tab.Pane eventKey="list">
            <RequestsList />
          </Tab.Pane>
        </Tab.Content>
      </Tab.Container>
    </Stack>
  );
}

Charts.propTypes = {
  activeTab: PropTypes.oneOf(['list', 'chart']).isRequired,
  setActiveTab: PropTypes.func.isRequired,
};
