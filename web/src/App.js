import { Container, Row } from 'react-bootstrap';
import Registration from './components/Registration';

function App() {
  return (
    <Container>
      <Row className='justify-content-center'>
        <Registration />        
      </Row>
    </Container>
  );
}

export default App;
