import { observer } from 'mobx-react-lite';
import { Modal } from 'react-bootstrap';
import PropTypes from 'prop-types';
import { useStore } from '../../Store/StoreProvider';

function UModal({
  content,
  options,
  hide,
  remove,
  id,
  isShown,
  onSubmit,
  onClose,
}) {
  const handleClose = () => {
    hide(id);
  };

  const onExited = () => {
    remove(id);
    onClose && onClose();
  };

  const handleSubmit = () => {
    hide(id);
    onSubmit && onSubmit();
  };

  return (
    <Modal show={isShown} onHide={handleClose} onExited={onExited} {...options}>
      {content.title && (
        <Modal.Header closeButton>
          <Modal.Title as="h5">
            {content.title({ handleClose, handleSubmit })}
          </Modal.Title>
        </Modal.Header>
      )}
      <Modal.Body>{content.body({ handleClose, handleSubmit })}</Modal.Body>
      {content.buttons && (
        <Modal.Footer>
          {content.buttons({ handleClose, handleSubmit })}
        </Modal.Footer>
      )}
    </Modal>
  );
}

UModal.propTypes = {
  content: PropTypes.shape({
    title: PropTypes.func,
    body: PropTypes.func.isRequired,
    buttons: PropTypes.func,
  }).isRequired,
  hide: PropTypes.func.isRequired,
  remove: PropTypes.func.isRequired,
  options: PropTypes.objectOf(PropTypes.any),
  id: PropTypes.string.isRequired,
  isShown: PropTypes.bool.isRequired,
  onSubmit: PropTypes.func,
  onClose: PropTypes.func,
};

UModal.defaultProps = {
  options: {},
  onSubmit: undefined,
  onClose: undefined,
};

function Modals() {
  const { modals } = useStore();
  return modals.modals.map((modalProps) => (
    <UModal
      {...modalProps}
      hide={modals.hideModal}
      remove={modals.removeModal}
      key={modalProps.id}
    />
  ));
}

export default observer(Modals);
