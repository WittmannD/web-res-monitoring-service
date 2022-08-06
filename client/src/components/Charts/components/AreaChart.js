import React, { useEffect, useState } from 'react';
import 'chartjs-adapter-moment';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
} from 'chart.js';
import moment from 'moment';
import { Line } from 'react-chartjs-2';
import { useParams } from 'react-router-dom';
import { getMonitorRequests } from '../../../http/api';
import ChartPlaceholder from './ChartPlaceholder';

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
);

export const getOptions = ({ labels }) => ({
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Response time for last 24 hours',
    },
  },
  scales: {
    x: {
      type: 'time',
      time: {
        tooltipFormat: '[request at ]HH:mm:ss',
        stepSize: 5 * Math.max(1, Math.floor(labels.length / 10)),
        unit: 'minute',
        displayFormats: {
          minute: 'HH:mm:ss',
        },
      },
      // min: moment(lastDateValue).subtract(5, 'hours'),
    },
    y: {
      offset: false,
    },
  },
});

const prepareData = (requests) => {
  const labels = [];
  const data = [];

  for (const request of requests) {
    labels.unshift(moment.utc(request.timestamp).local());
    data.unshift(request.elapsed);
  }

  return { labels, data };
};

export default function AreaChart() {
  const [isLoading, setIsLoading] = useState(true);
  const [chartData, setChartData] = useState({});
  const [chartOptions, setChartOptions] = useState({});
  const { monitorId } = useParams();

  const getData = async () => {
    const now = moment().utc();
    const dayBefore = moment(now).subtract(24, 'hours');

    const {
      content: { items: requestsData },
    } = await getMonitorRequests(monitorId, {
      datetime_start: dayBefore.toISOString(),
      datetime_end: now.toISOString(),
      per_page: 290,
      page: 1,
    });

    const { labels, data } = prepareData(requestsData);
    setChartData({
      labels,
      datasets: [
        {
          data,
          fill: true,
          label: 'Response time',
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
        },
      ],
    });
    setChartOptions(
      getOptions({
        labels,
      })
    );

    return () => {
      setIsLoading(true);
    };
  };

  useEffect(() => {
    getData().then(() => setIsLoading(false));
  }, []);

  return !isLoading ? (
    <Line options={chartOptions} data={chartData} type="line" />
  ) : (
    <ChartPlaceholder />
  );
}
