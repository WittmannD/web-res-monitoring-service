import { makeAutoObservable } from 'mobx';
import { v4 as uuid } from 'uuid';

export default class ModalsStore {
  constructor() {
    this._modals = [];

    makeAutoObservable(this);
    this.removeModal = this.removeModal.bind(this);
    this.createModal = this.createModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
  }

  createModal({
    content,
    options,
    onSubmit = null,
    onClose = null,
    id = uuid(),
  }) {
    const restModals = this._modals.filter((o) => o.id !== id);

    this._modals = [
      ...restModals,
      {
        id,
        content,
        options,
        onSubmit,
        onClose,
        isShown: true,
      },
    ];
  }

  removeModal(id) {
    const restModals = this._modals.filter((o) => o.id !== id);

    this._modals = [...restModals];
  }

  hideModal(id) {
    const modalIndex = this._modals.findIndex((o) => o.id === id);

    if (modalIndex !== -1) {
      this._modals[modalIndex].isShown = false;
    }
  }

  get modals() {
    return this._modals;
  }
}
