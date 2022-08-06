import { Placeholder, Stack, Table } from 'react-bootstrap';
import React from 'react';
import _ from 'lodash';
import styles from '../styles/RequestsList.module.scss';

export default function RequestsListPlaceholder() {
  return (
    <Stack direction="vertical" gap={2}>
      <Table bsPrefix={styles.table}>
        <thead>
          <Placeholder as="tr" animation="glow">
            <th>
              <Placeholder xs={2} bg="secondary" />
            </th>
            <th>
              <Placeholder xs={2} bg="secondary" />
            </th>
            <th>
              <Placeholder xs={3} bg="secondary" />
            </th>
          </Placeholder>
        </thead>
        <tbody>
          {_.range(0, 10, 1).map((n) => (
            <Placeholder key={n} as="tr" animation="glow">
              <td>
                <Placeholder xs={_.sample([3, 4])} bg="secondary" />
              </td>
              <td>
                <Placeholder xs={_.sample([4, 5])} bg="secondary" />
              </td>
              <td>
                <Placeholder xs={6} bg="secondary" />
              </td>
            </Placeholder>
          ))}
        </tbody>
      </Table>
      <Placeholder as={Stack} direction="horizontal" gap={2} animation="glow">
        <Placeholder.Button
          variant="outline-light"
          xs={4}
          bsPrefix="placeholder page-link"
        />
      </Placeholder>
    </Stack>
  );
}
