
import './App.css'
// import FilterButton from './components/FilterButton'
import SearchBar from './components/SearchBar'
import SelectCard from './components/SelectCard'


function App() {
  

  return (
    <>

    <SearchBar />
    {/* <FilterButton /> */}

    <div className="cards">
    <SelectCard />
    </div>
    </>
  )
}

export default App
