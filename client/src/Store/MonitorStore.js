import { makeAutoObservable, observable, action, computed } from 'mobx';

export default class MonitorStore {
  constructor() {
    this._monitors = [];
    this._current = null;

    makeAutoObservable(this, {
      _monitors: observable,
      _current: observable,

      setMonitors: action,
      setCurrentMonitor: action,
      addMonitor: action,
      removeMonitor: action,
      setMonitor: action,

      activeMonitorsCount: computed,
      pausedMonitorsCount: computed,
      upMonitorsCount: computed,
      downMonitorsCount: computed,
    });
  }

  setMonitors(data) {
    this._monitors = data;
  }

  setCurrentMonitor(data) {
    this._current = data;
  }

  addMonitor(data) {
    this._monitors = [data, ...this._monitors];
  }

  removeMonitor(id) {
    this._monitors = this._monitors.filter((o) => o.id !== id);

    if (this._current.id === id) {
      this._current = null;
    }
  }

  setMonitor(id, data) {
    const monitorIndex = this._monitors.findIndex((o) => o.id === id);

    if (monitorIndex !== -1) {
      this._monitors[monitorIndex] = data;
    }

    if (this._current.id === id) {
      this._current = data;
    }
  }

  get monitors() {
    return this._monitors;
  }

  get current() {
    return this._current;
  }

  get activeMonitorsCount() {
    return this._monitors.filter((monitor) => monitor.running).length;
  }

  get pausedMonitorsCount() {
    return this._monitors.filter((monitor) => !monitor.running).length;
  }

  get upMonitorsCount() {
    return this._monitors.filter(
      (monitor) => monitor.status === 'UP' && monitor.running
    ).length;
  }

  get downMonitorsCount() {
    return this._monitors.filter(
      (monitor) => monitor.status === 'DOWN' && monitor.running
    ).length;
  }
}
