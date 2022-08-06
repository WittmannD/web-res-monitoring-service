import { createContext, useContext, useMemo } from 'react';
import PropTypes from 'prop-types';
import UserStore from './UserStore';
import MonitorStore from './MonitorStore';
import ModalsStore from './ModalsStore';

export const StoreContext = createContext(null);

export default function StoreProvider({ children }) {
  const defaultValue = useMemo(
    () => ({
      user: new UserStore(),
      monitoring: new MonitorStore(),
      modals: new ModalsStore(),
    }),
    []
  );

  return (
    <StoreContext.Provider value={defaultValue}>
      {children}
    </StoreContext.Provider>
  );
}

StoreProvider.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]).isRequired,
};

export function useStore() {
  return useContext(StoreContext);
}
