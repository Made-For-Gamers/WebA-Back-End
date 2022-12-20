using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Models
{
    public class DeveloperModel
    {
        public int DeveloperId { get; set; }
        public UserModel Developer { get; set; }

        public int FeatureId { get; set; }
        public FeatureModel Feature { get; set; }

    }
}
