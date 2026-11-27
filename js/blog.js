(function(){
  const articles = [
    {
      id: 'b1',
      title: 'Top 10 Fastest Hypercars of 2026',
      category: 'Hypercars',
      readTime: '6 min read',
      cover: 'assets/images/cars/supercar-01.jpg',
      content: '<p>2026 continues the arms race of speed. From hybrid hypercars to aerodynamic monsters, the fastest machines push beyond 450 km/h in special configurations. This guide highlights what makes them quick: power density, downforce, and tire technology.</p><p>Expect brands like Bugatti, Koenigsegg, and Rimac to dominate discussions, while new challengers emerge from Europe and the Middle East.</p>'
    },
    {
      id: 'b2',
      title: 'EV Revolution vs V12 Engines',
      category: 'Industry',
      readTime: '7 min read',
      cover: 'assets/images/cars/ev-01.jpg',
      content: '<p>Electric drivetrains deliver instant torque and quiet speed, while V12 engines offer emotion, sound, and heritage. The future likely blends both: performance EVs for daily speed and limited-run combustion icons for collectors.</p>'
    },
    {
      id: 'b3',
      title: 'Best Luxury SUVs in India',
      category: 'Luxury',
      readTime: '5 min read',
      cover: 'assets/images/cars/luxury-01.jpg',
      content: '<p>Luxury SUVs combine comfort, presence, and capability. In India, popular picks include models from Mercedes-Benz, BMW, Audi, Volvo, and Land Rover — with strong after-sales and road presence being key factors.</p>'
    },
    {
      id: 'b4',
      title: 'Muscle Cars: Old School vs New School',
      category: 'Muscle',
      readTime: '5 min read',
      cover: 'assets/images/cars/muscle-01.jpg',
      content: '<p>Classic muscle cars focused on big displacement and straight-line fun. Modern muscle adds electronics, safety, and in some cases electrification — but the attitude remains.</p>'
    },
    {
      id: 'b5',
      title: 'How to Choose Your First Sports Car',
      category: 'Guide',
      readTime: '4 min read',
      cover: 'assets/images/cars/supercar-01.jpg',
      content: '<p>Start with budget, running costs, and usability. A balanced sports car can be more rewarding than an extreme hypercar you rarely drive.</p>'
    },
    {
      id: 'b6',
      title: 'Understanding Horsepower, Torque, and 0-60',
      category: 'Guide',
      readTime: '4 min read',
      cover: 'assets/images/cars/suv-01.jpg',
      content: '<p>Horsepower relates to sustained power, torque relates to pull, and 0-60 is influenced by traction, gearing, and weight. Together they tell a fuller performance story.</p>'
    },
    {
      id: 'b7',
      title: 'Best Budget Hatchbacks for City Life',
      category: 'Hatchback',
      readTime: '5 min read',
      cover: 'assets/images/cars/suv-01.jpg',
      content: '<p>Hatchbacks are practical, efficient, and easy to park. Look for safety ratings, service network, and fuel costs when buying in this segment.</p>'
    },
    {
      id: 'b8',
      title: 'Off-Road SUVs: What Actually Matters',
      category: 'SUV',
      readTime: '6 min read',
      cover: 'assets/images/cars/suv-01.jpg',
      content: '<p>Ground clearance, approach/departure angles, 4x4 systems, and tires matter more than horsepower when the road ends.</p>'
    }
  ];

  window.CarWorldsBlog = {
    getAll(){ return articles; }
  };
})();
