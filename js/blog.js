(function(){
  const articles = [
    {
      id: 'b1',
      title: 'Top 10 Fastest Hypercars of 2026',
      category: 'Hypercars',
      readTime: '6 min read',
      cover: 'assets/images/cars/bugatti-chiron.jpg',
      content: '<p>2026 continues the arms race of speed. From hybrid hypercars to aerodynamic monsters, the fastest machines push beyond 450 km/h in special configurations. This guide highlights what makes them quick: power density, downforce, and tire technology.</p><p>Expect brands like Bugatti, Koenigsegg, Rimac, and McLaren to dominate discussions, while new challengers emerge with electric powertrains.</p>'
    },
    {
      id: 'b2',
      title: 'EV Revolution vs V12 Engines',
      category: 'Industry',
      readTime: '7 min read',
      cover: 'assets/images/cars/tesla-model-s.jpg',
      content: '<p>Electric drivetrains deliver instant torque and quiet speed, while V12 engines offer emotion, sound, and heritage. The future likely blends both: performance EVs for daily speed and limited-run combustion icons for collectors.</p><p>From the Tesla Model S Plaid to the Ferrari 12Cilindri, both worlds have something extraordinary to offer.</p>'
    },
    {
      id: 'b3',
      title: 'Best Luxury SUVs in India',
      category: 'Luxury',
      readTime: '5 min read',
      cover: 'assets/images/cars/range-rover.jpg',
      content: '<p>Luxury SUVs combine comfort, presence, and capability. In India, popular picks include the Range Rover, Mercedes-Maybach GLS, BMW X7, and Volvo XC90 — with strong after-sales and road presence being key factors.</p>'
    },
    {
      id: 'b4',
      title: 'Muscle Cars: Old School vs New School',
      category: 'Muscle',
      readTime: '5 min read',
      cover: 'assets/images/cars/ford-mustang.jpg',
      content: '<p>Classic muscle cars focused on big displacement and straight-line fun. Modern muscle adds electronics, safety, and in some cases electrification — but the attitude remains. The Ford Mustang and Dodge Challenger still carry the torch.</p>'
    },
    {
      id: 'b5',
      title: 'How to Choose Your First Sports Car',
      category: 'Guide',
      readTime: '4 min read',
      cover: 'assets/images/cars/porsche-911.jpg',
      content: '<p>Start with budget, running costs, and usability. A balanced sports car like the Porsche 911 or Toyota GR86 can be more rewarding than an extreme hypercar you rarely drive. Consider insurance, service, and how you actually plan to use it.</p>'
    },
    {
      id: 'b6',
      title: 'Understanding Horsepower, Torque, and 0-60',
      category: 'Guide',
      readTime: '4 min read',
      cover: 'assets/images/cars/bmw-m4.jpg',
      content: '<p>Horsepower relates to sustained power, torque relates to pull, and 0-60 is influenced by traction, gearing, and weight. Together they tell a fuller performance story than any single number alone.</p>'
    },
    {
      id: 'b7',
      title: 'Best Budget Hatchbacks for City Life',
      category: 'Hatchback',
      readTime: '5 min read',
      cover: 'assets/images/cars/honda-civic-type-r.jpg',
      content: '<p>Hatchbacks are practical, efficient, and easy to park. Look for safety ratings, service network, and fuel costs when buying in this segment. From the Swift Sport to the Golf GTI, there is a hot hatch for every budget.</p>'
    },
    {
      id: 'b8',
      title: 'Off-Road SUVs: What Actually Matters',
      category: 'SUV',
      readTime: '6 min read',
      cover: 'assets/images/cars/mahindra-thar.jpg',
      content: '<p>Ground clearance, approach/departure angles, 4x4 systems, and tires matter more than horsepower when the road ends. Icons like the Jeep Wrangler, Land Rover Defender, and Mahindra Thar prove capability comes from engineering, not just numbers.</p>'
    }
  ];

  window.CarWorldsBlog = { getAll(){ return articles; } };
})();
