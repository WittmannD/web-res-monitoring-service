import _ from 'lodash';
import { useMemo } from 'react';

const usePagination = ({
  totalPages,
  activePage,
  paginationLength,
  paginationStart = 1,
}) =>
  useMemo(() => {
    const paginationEnd = totalPages;

    const half = Math.floor(paginationLength / 2);

    const leftBound = Math.min(
      Math.max(paginationStart, activePage - half),
      Math.max(paginationEnd - paginationLength + 1, paginationStart)
    );
    const rightBound = Math.max(
      Math.min(paginationEnd, activePage + half),
      Math.min(paginationLength, paginationEnd)
    );

    let range = _.range(paginationStart, totalPages + 1, 1);
    const left = _.take(range, leftBound - 1);
    const right = _.takeRight(range, paginationEnd - rightBound);

    range = _.drop(range, leftBound - 1);
    range = _.dropRight(range, paginationEnd - rightBound);

    return { leftRest: left, pagination: range, rightRest: right };
  }, [activePage, paginationLength, paginationStart]);

export default usePagination;
