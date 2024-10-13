import Dropdown from 'react-bootstrap/Dropdown';
//import DropdownButton from 'react-bootstrap/DropdownButton';
//import Container from 'react-bootstrap/Container';

function FilterButton() {
  return (
    
    <Dropdown>
      <Dropdown.Toggle variant="success" id="dropdown-basic">
        Filter
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Item href="#/action-1">Food</Dropdown.Item>
        <Dropdown.Item href="#/action-2">Electronics</Dropdown.Item>
        <Dropdown.Item href="#/action-3">Clothes</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default FilterButton;