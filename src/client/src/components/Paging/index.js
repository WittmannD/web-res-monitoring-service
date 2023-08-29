import { Pagination } from 'react-bootstrap';
import PropTypes from 'prop-types';
import { useMemo } from 'react';
import usePagination from '../../hooks/usePagination';

const paginationLength = 5;
const paginationStart = 1;

export default function Paging({ activePage, totalPages, onPageChange }) {
  const { leftRest, pagination, rightRest } = usePagination({
    totalPages,
    activePage,
    paginationLength,
    paginationStart,
  });

  const paginationEnd = totalPages;

  const isFirst = activePage === paginationStart;
  const isLast = activePage === Math.max(totalPages, paginationStart);

  const onNext = () => onPageChange(activePage + 1);
  const onPrevious = () => onPageChange(activePage - 1);

  const PaginationItem = (n) =>
    useMemo(
      () => (
        <Pagination.Item
          active={n === activePage}
          onClick={() => onPageChange(n)}
          key={n}
        >
          {n}
        </Pagination.Item>
      ),
      [n, activePage]
    );

  return (
    <Pagination>
      <Pagination.Prev disabled={isFirst} onClick={onPrevious} />
      {leftRest.length > 0 && (
        <>
          {PaginationItem(paginationStart)}
          {leftRest.length > 2 && <Pagination.Ellipsis disabled />}
          {leftRest.length === 2 && PaginationItem(paginationStart + 1)}
        </>
      )}
      {pagination.map((n) => PaginationItem(n))}
      {rightRest.length > 0 && (
        <>
          {rightRest.length === 2 && PaginationItem(paginationEnd - 1)}
          {leftRest.length > 2 && <Pagination.Ellipsis disabled />}
          {PaginationItem(paginationEnd)}
        </>
      )}
      <Pagination.Next disabled={isLast} onClick={onNext} />
    </Pagination>
  );
}

Paging.propTypes = {
  activePage: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
};
