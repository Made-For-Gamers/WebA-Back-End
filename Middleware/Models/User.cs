using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Datalayer.Models
{
    public class User
    {
        internal int Id { get; set; }
        public Guid UserId { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        internal string PasswordHash { get; set; }

        public List<UserClaim> Claims { get; set; } = new();
        public IEnumerable<Project> Projects { get; set; } 
    }
}
