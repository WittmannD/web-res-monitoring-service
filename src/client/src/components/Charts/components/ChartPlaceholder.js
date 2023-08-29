import { Spinner } from 'react-bootstrap';

export default function ChartPlaceholder() {
  return (
    <div className="h-80 d-flex align-items-center justify-content-center rounded-3 bg-light">
      <Spinner animation="border" variant="secondary" size="sm" />
    </div>
  );
}
